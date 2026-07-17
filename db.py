#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database module - PostgreSQL connection layer for the bot.
Replaces the SQLite layer with a psycopg2-based connection that preserves
the same interface used throughout bot.py (c_main.execute / fetchone / fetchall,
conn_main.commit, INSERT OR IGNORE / INSERT OR REPLACE semantics).
"""

import os
import re
import threading
import logging
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor, DictCursor

logger = logging.getLogger(__name__)

# ==================== Connection Configuration ====================
# Prefer the direct Postgres URL; fall back to Supabase env vars.
DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or os.environ.get("SUPABASE_DB_URL")
    or os.environ.get("POSTGRES_URL")
)

if not DATABASE_URL:
    # Build from Supabase env vars if available
    supa_url = os.environ.get("SUPABASE_URL") or os.environ.get("VITE_SUPABASE_URL")
    supa_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("VITE_SUPABASE_ANON_KEY")
    db_host = os.environ.get("POSTGRES_HOST") or os.environ.get("DB_HOST")
    db_port = os.environ.get("POSTGRES_PORT", "5432")
    db_name = os.environ.get("POSTGRES_DB", "postgres")
    db_user = os.environ.get("POSTGRES_USER", "postgres")
    db_pass = os.environ.get("POSTGRES_PASSWORD") or os.environ.get("DB_PASSWORD")
    if db_host and db_pass:
        DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL / SUPABASE_DB_URL is not set. "
        "Provide a PostgreSQL connection string in the environment."
    )

# Normalize postgres:// to postgresql:// for psycopg2
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", "10"))
DB_TIMEOUT = int(os.environ.get("DB_TIMEOUT", "30"))

# ==================== Connection Pool ====================
_pool_lock = threading.Lock()
_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=2,
                    maxconn=DB_POOL_SIZE,
                    dsn=DATABASE_URL,
                    cursor_factory=DictCursor,
                    connect_timeout=DB_TIMEOUT,
                )
                logger.info("PostgreSQL connection pool created")
    return _pool


def get_db():
    """Borrow a connection from the pool."""
    return _get_pool().getconn()


def return_db(conn):
    """Return a connection to the pool."""
    try:
        _get_pool().putconn(conn)
    except Exception:
        pass


# ==================== SQL Translation ====================
_SQLITE_PARAM_RE = re.compile(r"(?<![\w$])\?(?![\w$])")


def _translate_sql(sql: str) -> str:
    """Translate SQLite-flavored SQL to PostgreSQL-compatible SQL.

    Handles:
      - ? placeholders -> %s
      - INSERT OR IGNORE -> INSERT ... ON CONFLICT DO NOTHING
      - INSERT OR REPLACE -> INSERT ... ON CONFLICT ... DO UPDATE
    """
    # Placeholder conversion
    out = _SQLITE_PARAM_RE.sub("%s", sql)

    # INSERT OR IGNORE -> ON CONFLICT DO NOTHING
    m = re.match(r'^\s*INSERT\s+OR\s+IGNORE\s+INTO\s+([`"\w]+)\s*\(([^)]*)\)', out, re.IGNORECASE)
    if m:
        out = re.sub(r'^\s*INSERT\s+OR\s+IGNORE\s+', 'INSERT ', out, count=1, flags=re.IGNORECASE)
        if 'ON CONFLICT' not in out.upper():
            out = out + ' ON CONFLICT DO NOTHING'
        return out

    # INSERT OR REPLACE -> ON CONFLICT DO UPDATE (best-effort generic)
    m2 = re.match(r'^\s*INSERT\s+OR\s+REPLACE\s+INTO\s+([`"\w]+)\s*\(([^)]*)\)', out, re.IGNORECASE)
    if m2:
        table = m2.group(1).strip('`"')
        cols_str = m2.group(2)
        cols = [c.strip().strip('`"') for c in cols_str.split(',')]
        out = re.sub(r'^\s*INSERT\s+OR\s+REPLACE\s+', 'INSERT ', out, count=1, flags=re.IGNORECASE)
        if 'ON CONFLICT' not in out.upper():
            # Determine conflict target: prefer PRIMARY KEY via first column if it looks like an id/user_id
            conflict_col = cols[0] if cols else 'id'
            set_clause = ', '.join(
                f'{c} = EXCLUDED.{c}' for c in cols if c != conflict_col
            )
            if set_clause:
                out = out + f' ON CONFLICT ({conflict_col}) DO UPDATE SET {set_clause}'
            else:
                out = out + ' ON CONFLICT DO NOTHING'
        return out

    return out


# ==================== SQLite-compatibility Cursor Wrapper ====================
class RowWrapper:
    """Wraps a psycopg2 DictRow so it supports both tuple-style indexing (row[0])
    and attribute-style access (row.column_name), matching sqlite3.Row behavior."""

    __slots__ = ('_data', '_keys')

    def __init__(self, data, keys):
        self._data = data
        self._keys = keys

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._data.values())[key]
        return self._data[key]

    def __iter__(self):
        return iter(self._data.values())

    def __len__(self):
        return len(self._data)

    def keys(self):
        return self._keys

    def __contains__(self, key):
        return key in self._data

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __repr__(self):
        return f"RowWrapper({dict(self._data)})"


class CursorWrapper:
    """Wraps a psycopg2 cursor to mimic sqlite3 Cursor behavior:
      - execute() translates ? -> %s and INSERT OR IGNORE/REPLACE
      - fetchone()/fetchall() return RowWrapper objects
      - lastrowid returns the last inserted id via RETURNING
    """

    def __init__(self, cursor, conn_wrapper):
        self._cursor = cursor
        self._conn = conn_wrapper
        self.lastrowid = None
        self.rowcount = -1

    def execute(self, sql, params=()):
        translated = _translate_sql(sql)
        self._cursor.execute(translated, params if isinstance(params, (tuple, list)) else (params,))
        self.rowcount = self._cursor.rowcount
        self.lastrowid = None
        return self

    def executemany(self, sql, seq_of_params):
        translated = _translate_sql(sql)
        # psycopg2 executemany doesn't support ON CONFLICT well; use execute in loop
        for params in seq_of_params:
            self.execute(sql, params)
        return self

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        keys = [d[0] for d in self._cursor.description] if self._cursor.description else []
        return RowWrapper(dict(row), keys)

    def fetchall(self):
        rows = self._cursor.fetchall()
        if not rows:
            return []
        keys = [d[0] for d in self._cursor.description] if self._cursor.description else []
        return [RowWrapper(dict(r), keys) for r in rows]

    def fetchmany(self, size=None):
        rows = self._cursor.fetchmany(size) if size else self._cursor.fetchmany()
        if not rows:
            return []
        keys = [d[0] for d in self._cursor.description] if self._cursor.description else []
        return [RowWrapper(dict(r), keys) for r in rows]

    @property
    def description(self):
        return self._cursor.description

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass


class ConnectionWrapper:
    """Wraps a psycopg2 connection to mimic sqlite3 connection behavior.
    Exposes a shared .cursor (c_main equivalent) and .commit() that commits
    the underlying connection. Each .execute on the shared cursor reuses the
    same underlying psycopg2 cursor for compatibility with bot.py usage.
    """

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()
        self._wrapper = CursorWrapper(self._cursor, self)

    def execute(self, sql, params=()):
        """Direct execute on the shared cursor (matches c_main.execute usage)."""
        return self._wrapper.execute(sql, params)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        try:
            self._conn.rollback()
        except Exception:
            pass

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass
        try:
            self._conn.close()
        except Exception:
            pass

    def cursor(self):
        return CursorWrapper(self._conn.cursor(), self)


# ==================== Shared "main" Connection ====================
# bot.py uses a module-level conn_main / c_main. We provide a persistent
# connection wrapper that auto-recovers from closures.
_conn_main = None
_conn_main_lock = threading.Lock()


def _new_connection_wrapper():
    conn = get_db()
    return ConnectionWrapper(conn)


def get_main_connection():
    global _conn_main
    with _conn_main_lock:
        if _conn_main is None:
            _conn_main = _new_connection_wrapper()
        return _conn_main


def _reset_main_connection():
    global _conn_main
    with _conn_main_lock:
        if _conn_main is not None:
            try:
                _conn_main.close()
            except Exception:
                pass
            return_db(_conn_main._conn)
        _conn_main = None


# Lazy proxies so bot.py's `conn_main` and `c_main` references work.
class _ConnMainProxy:
    def __getattr__(self, name):
        return getattr(get_main_connection(), name)

    def commit(self):
        get_main_connection().commit()

    def execute(self, sql, params=()):
        return get_main_connection().execute(sql, params)

    def rollback(self):
        get_main_connection().rollback()

    def close(self):
        _reset_main_connection()


class _CMainProxy:
    def __getattr__(self, name):
        return getattr(get_main_connection()._wrapper, name)

    def execute(self, sql, params=()):
        try:
            return get_main_connection().execute(sql, params)
        except psycopg2.OperationalError:
            get_main_connection().rollback()
            _reset_main_connection()
            return get_main_connection().execute(sql, params)
        except psycopg2.Error:
            get_main_connection().rollback()
            raise

    def fetchone(self):
        return get_main_connection()._wrapper.fetchone()

    def fetchall(self):
        return get_main_connection()._wrapper.fetchall()

    @property
    def lastrowid(self):
        return get_main_connection()._wrapper.lastrowid

    @property
    def rowcount(self):
        return get_main_connection()._wrapper.rowcount


conn_main = _ConnMainProxy()
c_main = _CMainProxy()


# ==================== Initialization Helper ====================
def init_db():
    """Verify connectivity and return True on success."""
    try:
        cw = get_main_connection()
        cw.execute("SELECT 1")
        cw.commit()
        logger.info("PostgreSQL connection verified")
        return True
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        _reset_main_connection()
        return False
