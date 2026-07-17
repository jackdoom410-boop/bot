-- ============================================================
-- AK Bot - Complete PostgreSQL Schema (Supabase)
-- Run this once to create all tables the bot needs.
-- Safe to re-run: uses IF NOT EXISTS / ON CONFLICT.
-- ============================================================

-- ============ USERS ============
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    name TEXT,
    last_use TEXT,
    banned INTEGER DEFAULT 0,
    admin INTEGER DEFAULT 0,
    allowed INTEGER DEFAULT 0,
    created_at TEXT,
    total_requests INTEGER DEFAULT 0
);
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_users" ON users;
CREATE POLICY "anon_all_users" ON users FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_users" ON users;
CREATE POLICY "anon_insert_users" ON users FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_users" ON users;
CREATE POLICY "anon_update_users" ON users FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_users" ON users;
CREATE POLICY "anon_delete_users" ON users FOR DELETE TO anon, authenticated USING (true);

-- ============ ALLOWED_USERS ============
CREATE TABLE IF NOT EXISTS allowed_users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    name TEXT,
    added_by BIGINT,
    added_date TEXT
);
ALTER TABLE allowed_users ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_allowed_users" ON allowed_users;
CREATE POLICY "anon_all_allowed_users" ON allowed_users FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_allowed_users" ON allowed_users;
CREATE POLICY "anon_insert_allowed_users" ON allowed_users FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_allowed_users" ON allowed_users;
CREATE POLICY "anon_update_allowed_users" ON allowed_users FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_allowed_users" ON allowed_users;
CREATE POLICY "anon_delete_allowed_users" ON allowed_users FOR DELETE TO anon, authenticated USING (true);

-- ============ USER_PLATFORM ============
CREATE TABLE IF NOT EXISTS user_platform (
    user_id BIGINT PRIMARY KEY,
    platform TEXT DEFAULT 'android'
);
ALTER TABLE user_platform ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_user_platform" ON user_platform;
CREATE POLICY "anon_all_user_platform" ON user_platform FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_user_platform" ON user_platform;
CREATE POLICY "anon_insert_user_platform" ON user_platform FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_user_platform" ON user_platform;
CREATE POLICY "anon_update_user_platform" ON user_platform FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_user_platform" ON user_platform;
CREATE POLICY "anon_delete_user_platform" ON user_platform FOR DELETE TO anon, authenticated USING (true);

-- ============ GAMES_AF ============
CREATE TABLE IF NOT EXISTS games_af (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    display_name TEXT,
    package TEXT,
    dev_key TEXT,
    emoji TEXT
);
ALTER TABLE games_af ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_games_af" ON games_af;
CREATE POLICY "anon_all_games_af" ON games_af FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_games_af" ON games_af;
CREATE POLICY "anon_insert_games_af" ON games_af FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_games_af" ON games_af;
CREATE POLICY "anon_update_games_af" ON games_af FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_games_af" ON games_af;
CREATE POLICY "anon_delete_games_af" ON games_af FOR DELETE TO anon, authenticated USING (true);

-- ============ GAMES_SINGULAR ============
CREATE TABLE IF NOT EXISTS games_singular (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    display_name TEXT,
    package TEXT,
    app_key TEXT,
    emoji TEXT
);
ALTER TABLE games_singular ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_games_singular" ON games_singular;
CREATE POLICY "anon_all_games_singular" ON games_singular FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_games_singular" ON games_singular;
CREATE POLICY "anon_insert_games_singular" ON games_singular FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_games_singular" ON games_singular;
CREATE POLICY "anon_update_games_singular" ON games_singular FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_games_singular" ON games_singular;
CREATE POLICY "anon_delete_games_singular" ON games_singular FOR DELETE TO anon, authenticated USING (true);

-- ============ GAMES_ADJ ============
CREATE TABLE IF NOT EXISTS games_adj (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    display_name TEXT,
    app_token TEXT,
    emoji TEXT
);
ALTER TABLE games_adj ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_games_adj" ON games_adj;
CREATE POLICY "anon_all_games_adj" ON games_adj FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_games_adj" ON games_adj;
CREATE POLICY "anon_insert_games_adj" ON games_adj FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_games_adj" ON games_adj;
CREATE POLICY "anon_update_games_adj" ON games_adj FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_games_adj" ON games_adj;
CREATE POLICY "anon_delete_games_adj" ON games_adj FOR DELETE TO anon, authenticated USING (true);

-- ============ EVENTS_AF ============
CREATE TABLE IF NOT EXISTS events_af (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games_af(id) ON DELETE CASCADE,
    event_name TEXT,
    display_name TEXT,
    event_type TEXT,
    is_purchase INTEGER DEFAULT 0
);
ALTER TABLE events_af ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_events_af" ON events_af;
CREATE POLICY "anon_all_events_af" ON events_af FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_events_af" ON events_af;
CREATE POLICY "anon_insert_events_af" ON events_af FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_events_af" ON events_af;
CREATE POLICY "anon_update_events_af" ON events_af FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_events_af" ON events_af;
CREATE POLICY "anon_delete_events_af" ON events_af FOR DELETE TO anon, authenticated USING (true);

-- ============ EVENTS_SINGULAR ============
CREATE TABLE IF NOT EXISTS events_singular (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games_singular(id) ON DELETE CASCADE,
    event_name TEXT,
    display_name TEXT,
    event_type TEXT
);
ALTER TABLE events_singular ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_events_singular" ON events_singular;
CREATE POLICY "anon_all_events_singular" ON events_singular FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_events_singular" ON events_singular;
CREATE POLICY "anon_insert_events_singular" ON events_singular FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_events_singular" ON events_singular;
CREATE POLICY "anon_update_events_singular" ON events_singular FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_events_singular" ON events_singular;
CREATE POLICY "anon_delete_events_singular" ON events_singular FOR DELETE TO anon, authenticated USING (true);

-- ============ EVENTS_ADJ ============
CREATE TABLE IF NOT EXISTS events_adj (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games_adj(id) ON DELETE CASCADE,
    event_name TEXT,
    event_token TEXT,
    display_name TEXT,
    level_value INTEGER
);
ALTER TABLE events_adj ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_events_adj" ON events_adj;
CREATE POLICY "anon_all_events_adj" ON events_adj FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_events_adj" ON events_adj;
CREATE POLICY "anon_insert_events_adj" ON events_adj FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_events_adj" ON events_adj;
CREATE POLICY "anon_update_events_adj" ON events_adj FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_events_adj" ON events_adj;
CREATE POLICY "anon_delete_events_adj" ON events_adj FOR DELETE TO anon, authenticated USING (true);

-- ============ PROXIES ============
CREATE TABLE IF NOT EXISTS proxies (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE,
    proxy_type TEXT,
    proxy_host TEXT,
    proxy_port INTEGER,
    proxy_user TEXT,
    proxy_pass TEXT,
    created_date TEXT,
    last_used TEXT,
    usage_count INTEGER DEFAULT 0
);
ALTER TABLE proxies ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_proxies" ON proxies;
CREATE POLICY "anon_all_proxies" ON proxies FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_proxies" ON proxies;
CREATE POLICY "anon_insert_proxies" ON proxies FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_proxies" ON proxies;
CREATE POLICY "anon_update_proxies" ON proxies FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_proxies" ON proxies;
CREATE POLICY "anon_delete_proxies" ON proxies FOR DELETE TO anon, authenticated USING (true);

-- ============ FARM_TASKS ============
CREATE TABLE IF NOT EXISTS farm_tasks (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    task_name TEXT UNIQUE,
    platform TEXT,
    game_id INTEGER,
    game_name TEXT,
    start_level INTEGER,
    end_level INTEGER,
    total_days INTEGER,
    mode TEXT,
    current_day INTEGER,
    current_level INTEGER,
    status TEXT,
    created_date TEXT,
    last_run TEXT,
    aifa TEXT,
    gaid TEXT,
    uid TEXT,
    af_uid TEXT,
    gps_adid TEXT,
    idfa TEXT,
    idfv TEXT,
    att_status INTEGER,
    completed_levels INTEGER DEFAULT 0,
    failed_attempts INTEGER DEFAULT 0
);
ALTER TABLE farm_tasks ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_farm_tasks" ON farm_tasks;
CREATE POLICY "anon_all_farm_tasks" ON farm_tasks FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_farm_tasks" ON farm_tasks;
CREATE POLICY "anon_insert_farm_tasks" ON farm_tasks FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_farm_tasks" ON farm_tasks;
CREATE POLICY "anon_update_farm_tasks" ON farm_tasks FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_farm_tasks" ON farm_tasks;
CREATE POLICY "anon_delete_farm_tasks" ON farm_tasks FOR DELETE TO anon, authenticated USING (true);

-- ============ USER_STATS ============
CREATE TABLE IF NOT EXISTS user_stats (
    user_id BIGINT PRIMARY KEY,
    last_daily_reset TEXT,
    daily_requests INTEGER DEFAULT 0,
    total_af_requests INTEGER DEFAULT 0,
    total_adj_requests INTEGER DEFAULT 0,
    total_singular_requests INTEGER DEFAULT 0
);
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all_user_stats" ON user_stats;
CREATE POLICY "anon_all_user_stats" ON user_stats FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "anon_insert_user_stats" ON user_stats;
CREATE POLICY "anon_insert_user_stats" ON user_stats FOR INSERT TO anon, authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "anon_update_user_stats" ON user_stats;
CREATE POLICY "anon_update_user_stats" ON user_stats FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "anon_delete_user_stats" ON user_stats;
CREATE POLICY "anon_delete_user_stats" ON user_stats FOR DELETE TO anon, authenticated USING (true);

-- ============ INDEXES ============
CREATE INDEX IF NOT EXISTS idx_users_allowed ON users(allowed);
CREATE INDEX IF NOT EXISTS idx_users_banned ON users(banned);
CREATE INDEX IF NOT EXISTS idx_farm_tasks_user ON farm_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_farm_tasks_status ON farm_tasks(status);
CREATE INDEX IF NOT EXISTS idx_events_af_game ON events_af(game_id);
CREATE INDEX IF NOT EXISTS idx_events_adj_game ON events_adj(game_id);
CREATE INDEX IF NOT EXISTS idx_events_singular_game ON events_singular(game_id);
CREATE INDEX IF NOT EXISTS idx_proxies_user ON proxies(user_id);
CREATE INDEX IF NOT EXISTS idx_user_platform ON user_platform(user_id);

-- ============ BOT USER ROLE ============
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bot_user') THEN
        CREATE ROLE bot_user LOGIN PASSWORD 'akbot2025secure' NOSUPERUSER NOCREATEDB NOCREATEROLE BYPASSRLS;
    ELSE
        ALTER ROLE bot_user LOGIN PASSWORD 'akbot2025secure' BYPASSRLS;
    END IF;
END $$;
GRANT USAGE ON SCHEMA public TO bot_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO bot_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bot_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO bot_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO bot_user;

-- ============ SEED ADMINS ============
INSERT INTO users (user_id, username, name, admin, allowed, created_at)
VALUES (6075014046, 'admin', 'Admin', 1, 1, '2025-01-01')
ON CONFLICT (user_id) DO NOTHING;
INSERT INTO allowed_users (user_id, username, name, added_by, added_date)
VALUES (6075014046, 'admin', 'Admin', 6075014046, '2025-01-01')
ON CONFLICT (user_id) DO NOTHING;
INSERT INTO users (user_id, username, name, admin, allowed, created_at)
VALUES (8114043468, 'admin2', 'Admin2', 1, 1, '2025-01-01')
ON CONFLICT (user_id) DO NOTHING;
INSERT INTO allowed_users (user_id, username, name, added_by, added_date)
VALUES (8114043468, 'admin2', 'Admin2', 6075014046, '2025-01-01')
ON CONFLICT (user_id) DO NOTHING;
INSERT INTO user_platform (user_id, platform) VALUES (6075014046, 'android') ON CONFLICT (user_id) DO NOTHING;
INSERT INTO user_platform (user_id, platform) VALUES (8114043468, 'android') ON CONFLICT (user_id) DO NOTHING;
