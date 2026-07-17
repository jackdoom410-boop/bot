#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed script: inserts all the initial games and events data into PostgreSQL.
This mirrors the AF_GAMES, SINGULAR_GAMES, ADJ_GAMES lists and the
add_af_events / add_singular_events / add_adj_events functions from bot.py.
Idempotent: uses ON CONFLICT DO NOTHING so re-running is safe.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = False
cur = conn.cursor()


def upsert_game(table, cols, values):
    placeholders = ", ".join(["%s"] * len(values))
    col_list = ", ".join(cols)
    cur.execute(
        f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) "
        f"ON CONFLICT (name) DO NOTHING",
        values,
    )


def get_game_id(table, name):
    cur.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))
    row = cur.fetchone()
    return row[0] if row else None


def upsert_event(table, cols, values):
    placeholders = ", ".join(["%s"] * len(values))
    col_list = ", ".join(cols)
    cur.execute(
        f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) "
        f"ON CONFLICT DO NOTHING",
        values,
    )


# ==================== AppsFlyer Games ====================
AF_GAMES = [
    ("dice_dream", "🎲 Dice Dreams", "com.superplaystudios.dicedreams", "Hn5qYjVAaRNJYDcwF4LaWF", "🎲"),
    ("domino_dreams", "🃏 Domino Dreams", "com.screenshake.dominodreams", "Hn5qYjVAaRNJYDcwF4LaWF", "🃏"),
    ("buzzle_chaos", "🎲 Buzzle Chaos", "com.global.pnck", "ZnhUvonKa6qF9xhgt7GcBQ", "🎲"),
    ("coin_master", "🎲 Coin Master", "com.moonactive.coinmaster", "H3KjoCRVTiVgA5mWSAHtCe", "🎲"),
    ("royal_match", "👑 Royal Match", "com.dreamgames.royalmatch", "B27HnbGEcbWC2fv79DDhcb", "👑"),
    ("merge_gardens", "🌺 Merge Gardens", "com.futureplay.mergematch", "nr8SibwpFjcKGBQNpDdttd", "🌺"),
    ("highroller_vegas", "🎲 HIGHROLLER Vegas", "com.lynxgames.hrv", "sSpBC5SKPKEV8fbZJgw6vM", "🎲"),
    ("rock_n_cash", "💰 Rock N Cash Casino", "net.flysher.rockncash", "W5VWPj5fbCGABtk59TsmJQ", "💰"),
    ("coinchef", "🍳 COINCHEF", "com.FortuneMine.CuisineMaster", "im6mgZbZJsHKGVowkkxkGm", "🍳"),
    ("blackjack21", "🃏 Blackjack 21", "com.kamagames.blackjack", "YbczyDZZmXbxwpYYyJgqTQ", "🃏"),
    ("sunshine_island", "🏝️ Sunshine Island", "com.newmoonproduction.sunshineisland", "FtaT5WH9rMJjJkMd4LfBCT", "🏝️"),
    ("farmville3", "🌾 Farmville 3", "com.zynga.FarmVille2CountryEscape", "438VCPmX2ZLYvsDPfGLZXb", "🌾"),
    ("disney_solitaire", "🎲 Disney Solitaire", "com.superplaystudios.disneysolitairedreams", "Hn5qYjVAaRNJYDcwF4LaWF", "🎲"),
    ("matching_story", "🎲 Matching Story", "com.joycastle.mergematch", "v2w2tuNCNaBNXvFJgRGPRW", "🎲"),
    ("nations_of_darkness", "🎲 Nations of Darkness", "com.allstarunion.nod", "x88hdqNmd8vALRmRMhgY4Q", "🎲"),
    ("hero_wars", "🎲 Hero Wars", "com.nexters.herowars", "MGPcVAUzD9XqbwAY6q7KMf", "🎲"),
    ("zombie_waves", "🧟 Zombie Waves", "com.ddup.zombiewaves.zw", "wiQMRPvGaAYTGBCgM5yN9N", "🧟"),
]

for g in AF_GAMES:
    upsert_game("games_af", ["name", "display_name", "package", "dev_key", "emoji"], list(g))


def add_af_events():
    dd = get_game_id("games_af", "dice_dream")
    if dd:
        for ev in [
            ("af_kingdom_3_restored", "🏰 Kingdom 3", "kingdom", 0),
            ("af_kingdom_18_restored", "🏰 Kingdom 18", "kingdom", 0),
            ("af_kingdom_5_restored", "🏰 Kingdom 5", "kingdom", 0),
        ]:
            upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                         [dd, ev[0], ev[1], ev[2], ev[3]])

    dom = get_game_id("games_af", "domino_dreams")
    if dom:
        for area in range(1, 6):
            upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                         [dom, f"af_area_{area}_completed", f"🗺️ Area {area}", "area", 0])
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [dom, "af_level_100_completed", "🏆 Level 100", "level", 0])

    rm = get_game_id("games_af", "royal_match")
    if rm:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [rm, "level_3", "🏆 Level 3", "level", 0])
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [rm, "area_2", "🗺️ Area 2", "area", 0])

    mg = get_game_id("games_af", "merge_gardens")
    if mg:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [mg, "Incent_Player_Level_Up_2", "⭐ Player Level Up 2", "level", 0])
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [mg, "Incent_IAP_gems2", "💎 IAP Gems 2", "purchase", 1])

    hr = get_game_id("games_af", "highroller_vegas")
    if hr:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [hr, "app_level_achieved_5", "🎯 Level 5", "level", 0])

    rnc = get_game_id("games_af", "rock_n_cash")
    if rnc:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [rnc, "v3_rnc_level_up_10_S2S", "🎰 Level Up 10", "level", 0])

    cc = get_game_id("games_af", "coinchef")
    if cc:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [cc, "level2_completed", "🍳 Level 2 Completed", "level", 0])

    bj = get_game_id("games_af", "blackjack21")
    if bj:
        for ev in [
            ("30levelup", "🏆 Level 30", "level", 0),
            ("2level", "🃏 Level 2", "level", 0),
            ("5levelup", "🃏 Level 5", "level", 0),
        ]:
            upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                         [bj, ev[0], ev[1], ev[2], ev[3]])

    si = get_game_id("games_af", "sunshine_island")
    if si:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [si, "af_level5_achieved", "🏝️ Level 5", "level", 0])

    fv = get_game_id("games_af", "farmville3")
    if fv:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [fv, "Player_Level9", "⭐ Level 9", "level", 0])

    cm = get_game_id("games_af", "coin_master")
    if cm:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [cm, "village_1_complete", "🏠 Village 1 Complete", "level", 0])

    ds = get_game_id("games_af", "disney_solitaire")
    if ds:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [ds, "af_level_100_completed", "⭐ Level 100", "level", 0])
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [ds, "af_area_22_completed", "🗺️ Area 22", "area", 0])

    hw = get_game_id("games_af", "hero_wars")
    if hw:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [hw, "levelup5", "⭐ Level Up 5", "level", 0])

    zw = get_game_id("games_af", "zombie_waves")
    if zw:
        upsert_event("events_af", ["game_id", "event_name", "display_name", "event_type", "is_purchase"],
                     [zw, "af_zw_lv5", "🧟 Level 5", "level", 0])


add_af_events()

# ==================== Singular Games ====================
SINGULAR_GAMES = [
    ("animals_coins", "🦁 Animals & Coins", "com.innplaylabs.animalkingdomraid", "innplay_labs_33d87c9b", "🦁"),
    ("time_master", "⏰ Time Master", "com.firefog.timemaster", "myappfree_spa_38e49215", "⏰"),
    ("beast_go", "🐉 Beast Go", "com.ninthart.board.beastgo", "myappfree_spa_38e49215", "🐉"),
    ("coin_fantasy", "💰 Coin Fantasy", "com.okvision.coinfantasy", "myappfree_spa_38e49215", "💰"),
    ("dragon_farm", "🐉 Dragon Farm", "com.dragon.escape.island.adventure", "myappfree_spa_38e49215", "🐉"),
    ("box_cat_jam", "🐱 Box Cat Jam", "com.actionfit.blockcat", "actionfit_adc62229", "🐱"),
    ("idle_soap", "🧼 Idle Soap ASMR", "games.midnite.isa", "myappfree_spa_38e49215", "🧼"),
    ("superheroes_idle", "🦸 Superheroes Idle RPG", "games.midnite.sid", "myappfree_spa_38e49215", "🦸"),
    ("survivor_idle", "🏃 Survivor Idle Run", "games.midnite.sri", "myappfree_spa_38e49215", "🏃"),
    ("pop_slots", "🎰 POP Slots", "com.playstudios.popslots", "playstudios_3852f898", "🎰"),
    ("mgm_slots", "🎰 MGM Slots Live", "com.playstudios.showstar", "playstudios_3852f898", "🎰"),
    ("myvegas", "🎰 myVEGAS Slots", "com.playstudios.myvegas", "playstudios_3852f898", "🎰"),
    ("power_spin", "💪 Power Spin Quest", "com.braingames.powerquest", "brain_games_a7dde873", "💪"),
    ("sweet_jam", "🍯 Sweet Jam!", "puzzle.game.sweetjam", "myappfree_spa_38e49215", "🍯"),
    ("matching_go", "🔗 Matching Go!", "com.matchinggo.puzzlegames", "xinagyi_f4545a5d", "🔗"),
    ("screw_out", "🔧 Screw Out Factory 3D", "com.ntt.screw.out.factory", "puzzle_studios_4d38bec9", "🔧"),
    ("hole_collect", "🕳️ Hole Collect", "com.ntt.hole.collect.objects", "puzzle_studios_4d38bec9", "🕳️"),
    ("tetris_block", "🧩 Tetris Block Party", "com.playstudios.tetrisblockparty", "playstudios_3852f898", "🧩"),
    ("word_madness", "📖 Word Madness", "com.word.madness", "brain_games_a7dde873", "📖"),
    ("word_wise", "📖 Word Wise", "com.playx.wordwise.crossword", "myappfree_spa_38e49215", "📖"),
    ("eatventure", "🍔 Eatventure", "com.hwqgrhhjfd.idlefastfood", "lessmore_edff53fc", "🍔"),
]

for g in SINGULAR_GAMES:
    upsert_game("games_singular", ["name", "display_name", "package", "app_key", "emoji"], list(g))


def add_singular_events():
    def ev(game_name, event_name, display_name, event_type):
        gid = get_game_id("games_singular", game_name)
        if gid:
            upsert_event("events_singular", ["game_id", "event_name", "display_name", "event_type"],
                         [gid, event_name, display_name, event_type])

    ev("animals_coins", "Reach Level 3", "⏰ leve 3", "level")
    ev("time_master", "mn_location_1", "⏰ location 1", "level")
    ev("beast_go", "sng_level_achieved", "🐉 sng_level_achieved", "level")
    ev("coin_fantasy", "mn_level_", "💰 mn_level_", "level")
    ev("dragon_farm", "mn_level_", "🐉 mn_level_", "level")
    ev("box_cat_jam", "First_attempt_level_", "🐱 First_attempt_level_", "level")
    ev("idle_soap", "soap_unlocked", "🧼 soap_unlocked", "unlock")
    ev("superheroes_idle", "mn_cheater_level_achieved", "🦸 mn_cheater_level_achieved", "level")
    ev("survivor_idle", "sng_level_achieved", "🏃 sng_level_achieved", "level")
    ev("pop_slots", "level", "🎰 level", "level")
    ev("mgm_slots", "level", "🎰 level", "level")
    ev("myvegas", "level", "🎰 level", "level")
    ev("power_spin", "level_ended_", "💪 level_ended_", "level")
    ev("sweet_jam", "sng_level_achieved", "🍯 sng_level_achieved", "level")
    ev("matching_go", "user_level_complete_", "🔗 user_level_complete_", "level")
    ev("matching_go", "ad_show_", "📺 ad_show_", "ad")
    ev("hole_collect", "map_unlocked", "🗺️ map_unlocked", "unlock")
    ev("hole_collect", "sng_level_achieved", "🕳️ sng_level_achieved", "level")
    ev("tetris_block", "level_", "🧩 level_", "level")
    ev("word_madness", "_levels_completed", "📖 _levels_completed", "level")
    ev("word_wise", "mn_level_", "📖 mn_level_", "level")
    ev("eatventure", "restaurant_unlocked", "🍔 restaurant_unlocked", "unlock")
    ev("eatventure", "lm_restaurant_completion", "🍔 lm_restaurant_completion", "complete")


add_singular_events()

# ==================== Adjust Games ====================
ADJ_GAMES = [
    ("get_color", "🎨 Get Color", "367kicwptj5s", "🎨"),
    ("merge_blocks", "🔲 2048 X2 Merge Blocks", "367kicwptj5s", "🔲"),
    ("puzzle2248", "🧩 2248 Puzzle", "367kicwptj5s", "🧩"),
    ("alice_blastland", "🌸 Alice in Blastland", "367kicwptj5s", "🌸"),
    ("army_tycoon", "🎖️ Army Tycoon", "367kicwptj5s", "🎖️"),
    ("battle_night", "⚔️ Battle Night", "367kicwptj5s", "⚔️"),
    ("berry_factory", "🍓 Berry Factory Tycoon", "367kicwptj5s", "🍓"),
    ("big_card_solitaire", "🃏 Big Card Solitaire", "367kicwptj5s", "🃏"),
    ("bingo_aloha", "🍍 Bingo Aloha", "367kicwptj5s", "🍍"),
    ("bingo_showdown", "🎯 Bingo Showdown", "367kicwptj5s", "🎯"),
    ("blast_friends", "💥 Blast Friends", "367kicwptj5s", "💥"),
    ("block_blitz", "🧱 Block Blitz", "367kicwptj5s", "🧱"),
    ("block_joy", "🎮 Block Joy Puzzle", "367kicwptj5s", "🎮"),
    ("gems_adventure", "💎 Gems Adventure", "367kicwptj5s", "💎"),
    ("bravo_slots", "🎰 Bravo Classic Slots", "367kicwptj5s", "🎰"),
    ("cash_storm", "🌪️ Cash Storm", "367kicwptj5s", "🌪️"),
    ("climb_mountain", "⛰️ Climb the Mountain", "367kicwptj5s", "⛰️"),
    ("clock_maker", "⏰ Clock Maker", "367kicwptj5s", "⏰"),
    ("clone_evolution", "🧬 Clone Evolution", "367kicwptj5s", "🧬"),
    ("clubbillion", "🎲 Clubbillion Vegas", "367kicwptj5s", "🎲"),
    ("color_water_sort", "🎨 Color Water Sort", "367kicwptj5s", "🎨"),
]

for g in ADJ_GAMES:
    upsert_game("games_adj", ["name", "display_name", "app_token", "emoji"], list(g))


def add_adj_events():
    def add_list(game_name, events):
        gid = get_game_id("games_adj", game_name)
        if not gid:
            return
        for ev in events:
            upsert_event("events_adj", ["game_id", "event_name", "event_token", "display_name", "level_value"],
                         [gid, ev[0], ev[1], ev[2], ev[3]])

    # Get Color
    add_list("get_color", [
        (f"level_{lvl}", token, f"🏆 Level {lvl}", lvl)
        for lvl, token in [
            (15, "8t8nb3"), (30, "uwq9v8"), (50, "fdlgyk"), (75, "dwhyjz"), (80, "34vgez"),
            (100, "txq8if"), (120, "lwhvaj"), (150, "iatv2g"), (200, "stpy1k"), (300, "53lena"),
            (400, "dbdy8l"), (500, "3i4yf5"), (700, "pwd51u"), (1000, "4o9jbt"),
        ]
    ])

    # 2048 X2 Merge Blocks
    add_list("merge_blocks", [
        ("event_callback_yd6777", "yd6777", "Reach step 5", 5),
        ("event_callback_8mpa1x", "8mpa1x", "Step 10", 10),
        ("event_callback_j9tstz", "j9tstz", "Step 25", 25),
        ("event_callback_g3mipt", "g3mipt", "Step 50", 50),
        ("event_callback_v197np", "v197np", "Step 100", 100),
        ("event_callback_vbwc0z", "vbwc0z", "Step 250", 250),
        ("event_callback_j7pzey", "j7pzey", "Step 500", 500),
        ("event_callback_47euyf", "47euyf", "Step 1000", 1000),
        ("event_callback_jom3es", "jom3es", "Make a purchase", 0),
        ("event_callback_2i73t2", "2i73t2", "Purchase", 0),
    ])

    # 2248 Puzzle
    add_list("puzzle2248", [
        ("event_callback_lumf2i", "lumf2i", "Level 10", 10),
        ("event_callback_p08k2f", "p08k2f", "Level 25", 25),
        ("event_callback_cciiv6", "cciiv6", "Level 50", 50),
        ("event_callback_yysyts", "yysyts", "Level 100", 100),
        ("event_callback_dhwefa", "dhwefa", "Level 250", 250),
        ("event_callback_hn8yew", "hn8yew", "Level 500", 500),
        ("event_callback_igqmwt", "igqmwt", "Level 1000", 1000),
        ("event_callback_236tr52", "236tr52", "Session", 0),
    ])

    # Alice in Blastland
    add_list("alice_blastland", [
        ("event_callback_uefzz6", "uefzz6", "Reach Level 5", 5),
        ("event_callback_15h2c4", "15h2c4", "Level 15", 15),
        ("event_callback_x2o8is", "x2o8is", "First time deposit", 0),
        ("event_callback_dndphq", "dndphq", "Reach Level 30", 30),
        ("event_callback_5oolhi", "5oolhi", "Reach Level 50", 50),
        ("event_callback_l5p54c", "l5p54c", "Reach Level 100", 100),
        ("event_callback_yhj1lm", "yhj1lm", "Level 200", 200),
        ("event_callback_i4juxt", "i4juxt", "Level 300", 300),
        ("event_callback_oftnes", "oftnes", "Level 500", 500),
        ("event_callback_z8ovou", "z8ovou", "Level 750", 750),
        ("event_callback_qww7m6", "qww7m6", "Level 1000", 1000),
        ("event_callback_25764", "25764", "Session", 0),
    ])

    # Army Tycoon
    add_list("army_tycoon", [
        ("event_callback_ucfrab", "ucfrab", "Unlock Artillery Course", 1),
        ("event_callback_kcii8f", "kcii8f", "Unlock Tank Course", 2),
        ("event_callback_1tgiij", "1tgiij", "Unlock Indoor Shooting Range", 3),
        ("event_callback_x2b508", "x2b508", "Unlock Helicopter Course", 4),
        ("event_callback_afpgpn", "afpgpn", "Event", 5),
        ("event_callback_24260", "24260", "Session", 0),
    ])

    # Battle Night
    add_list("battle_night", [
        ("event_callback_wdu1px", "wdu1px", "Collect 2 Purple Heroes", 2),
        ("event_callback_at7h8t", "at7h8t", "Purchase Month Card", 0),
        ("event_callback_f6z6gr", "f6z6gr", "Complete Chapter 6", 6),
        ("event_callback_8no4ma", "8no4ma", "Buy Login Premium Pass", 0),
        ("event_callback_jb6urh", "jb6urh", "Collect 1 Orange Hero", 1),
        ("event_callback_lltjkz", "lltjkz", "2 Orange Hero", 2),
        ("event_callback_9dy8xg", "9dy8xg", "4 Orange Hero", 4),
        ("event_callback_z8vm09", "z8vm09", "6 Orange Hero", 6),
        ("event_callback_98bp74", "98bp74", "9 Orange Hero", 9),
        ("event_callback_9aqu0l", "9aqu0l", "Reach VIP Level 4", 4),
        ("event_callback_36w4u0", "36w4u0", "12 Orange Hero", 12),
        ("event_callback_xjcc3q", "xjcc3q", "15 Orange Hero", 15),
        ("event_callback_4g2o7u", "4g2o7u", "1 Red Hero", 1),
    ])

    # Berry Factory
    add_list("berry_factory", [
        ("event_callback_vex04j", "vex04j", "Reach Dessert Factory", 1),
        ("event_callback_f28p6w", "f28p6w", "Reach Candy Combine", 2),
        ("event_callback_rsrv4q", "rsrv4q", "Reach Jelly Concern", 3),
        ("event_callback_rktc9a", "rktc9a", "Upgrade Glazer to Maximum", 4),
        ("event_callback_32t74", "32t74", "Session", 0),
    ])

    # Big Card Solitaire
    add_list("big_card_solitaire", [
        ("event_callback_y0oh58", "y0oh58", "First Time Deposit", 0),
        ("event_callback_58fm8f", "58fm8f", "Reach Level 15", 15),
        ("event_callback_iecaaf", "iecaaf", "Level 20", 20),
        ("event_callback_i31lvg", "i31lvg", "Level 30", 30),
        ("event_callback_vjrg9q", "vjrg9q", "Collect 3K Coins", 3000),
        ("event_callback_1fiiml", "1fiiml", "Collect 5K Coins", 5000),
        ("event_callback_rbxsf1", "rbxsf1", "Collect 7K Coins", 7000),
        ("event_callback_i4avja", "i4avja", "10K Coins", 10000),
        ("event_callback_j2y6j9", "j2y6j9", "20K Coins", 20000),
        ("event_callback_r5um2u", "r5um2u", "50K Coins", 50000),
        ("event_callback_bbyp36", "bbyp36", "100K Coins", 100000),
        ("event_callback_b8gfs7", "b8gfs7", "200K Coins", 200000),
        ("event_callback_rb2zo3", "rb2zo3", "400K Coins", 400000),
    ])

    # Bingo Aloha
    add_list("bingo_aloha", [
        ("event_callback_tr4vq2", "tr4vq2", "Reach Level 20", 20),
        ("event_callback_f82iiq", "f82iiq", "Level 30", 30),
        ("event_callback_ifxzih", "ifxzih", "Level 40", 40),
        ("event_callback_3yza9s", "3yza9s", "Level 50", 50),
        ("event_callback_pk6qyf", "pk6qyf", "Bonus: Level 60 within 3 days", 60),
        ("event_callback_w5tltt", "w5tltt", "Level 80", 80),
        ("event_callback_189lri", "189lri", "Level 120", 120),
        ("event_callback_3g5fjn", "3g5fjn", "Level 150", 150),
        ("event_callback_2vj74s", "2vj74s", "Bonus: Level 200 within 6 days", 200),
        ("event_callback_ccm57s", "ccm57s", "Level 300", 300),
        ("event_callback_pxvvbe", "pxvvbe", "Level 400", 400),
        ("event_callback_uqst83", "uqst83", "Level 500", 500),
        ("event_callback_3wfbqv", "3wfbqv", "Purchase $19.9", 0),
        ("event_callback_ckugaz", "ckugaz", "Purchase $9.99", 0),
        ("event_callback_uvz4f0", "uvz4f0", "Purchase $4.99", 0),
    ])

    # Bingo Showdown
    add_list("bingo_showdown", [
        ("event_callback_w10qxm", "w10qxm", "First Bingo", 1),
        ("event_callback_3jdb4n", "3jdb4n", "Reach Level 2", 2),
        ("event_callback_njnr15", "njnr15", "Level 3", 3),
        ("event_callback_2sv8qt", "2sv8qt", "Level 5", 5),
        ("event_callback_14h0b2", "14h0b2", "Level 10", 10),
        ("event_callback_livykp", "livykp", "Level 15", 15),
        ("event_callback_95ye13", "95ye13", "Level 20", 20),
        ("event_callback_fjp3vm", "fjp3vm", "Level 25", 25),
        ("event_callback_upmo7s", "upmo7s", "Level 50", 50),
        ("event_callback_jkpze3", "jkpze3", "First Purchase", 0),
    ])

    # Blast Friends
    add_list("blast_friends", [
        ("event_callback_v5zsay", "v5zsay", "Reach Level 20", 20),
        ("event_callback_qco1yc", "qco1yc", "Level 50", 50),
        ("event_callback_nmbpbj", "nmbpbj", "Level 100", 100),
        ("event_callback_7tcb9y", "7tcb9y", "Level 250", 250),
        ("event_callback_a0tksk", "a0tksk", "Level 500", 500),
        ("event_callback_r9ojpu", "r9ojpu", "Level 1000", 1000),
        ("event_callback_8q1rrv", "8q1rrv", "Level 2000", 2000),
    ])

    # Block Blitz
    add_list("block_blitz", [
        ("event_callback_z9gmw7", "z9gmw7", "Win Journey Level 5", 5),
        ("event_callback_erj7x3", "erj7x3", "Level 10", 10),
        ("event_callback_1v5jpk", "1v5jpk", "Level 20", 20),
        ("event_callback_1puzhk", "1puzhk", "Level 30", 30),
        ("event_callback_fxhwo0", "fxhwo0", "Level 40", 40),
        ("event_callback_bqkl2c", "bqkl2c", "Level 50", 50),
        ("event_callback_tum80y", "tum80y", "Level 70", 70),
        ("event_callback_nm5hzf", "nm5hzf", "Level 100", 100),
        ("event_callback_ulzxtz", "ulzxtz", "Level 150", 150),
        ("event_callback_q7kns1", "q7kns1", "Level 300", 300),
        ("event_callback_uf24fv", "uf24fv", "Level 500", 500),
        ("event_callback_vjp76b", "vjp76b", "Level 700", 700),
        ("event_callback_nxjpvy", "nxjpvy", "Level 1000", 1000),
        ("event_callback_1020304", "1020304", "First Time Purchase", 0),
    ])

    # Block Joy
    add_list("block_joy", [
        ("event_callback_dvo8mu", "dvo8mu", "Level 5", 5),
        ("event_callback_r45ld3", "r45ld3", "Level 10", 10),
        ("event_callback_61mki6", "61mki6", "Level 20", 20),
        ("event_callback_15q1fg", "15q1fg", "Level 30", 30),
        ("event_callback_1ziiag", "1ziiag", "Level 50", 50),
        ("event_callback_yh508k", "yh508k", "Level 70", 70),
        ("event_callback_3gxgyp", "3gxgyp", "Level 100", 100),
        ("event_callback_vev8ur", "vev8ur", "Level 150", 150),
        ("event_callback_nazx5v", "nazx5v", "Level 300", 300),
        ("event_callback_q98rl6", "q98rl6", "Level 500", 500),
        ("event_callback_v1htdn", "v1htdn", "Level 700", 700),
        ("event_callback_soa9vy", "soa9vy", "Level 1000", 1000),
        ("event_callback_c8ck9d", "c8ck9d", "First Purchase", 0),
    ])

    # Gems Adventure
    add_list("gems_adventure", [
        ("event_callback_dwowyx", "dwowyx", "Score 3K", 3000),
        ("event_callback_h2e11l", "h2e11l", "Score 5K", 5000),
        ("event_callback_25ud1c", "25ud1c", "Score 10K", 10000),
        ("event_callback_3vdhft", "3vdhft", "Score 25K", 25000),
        ("event_callback_amhlay", "amhlay", "Score 50K", 50000),
        ("event_callback_mkuzzm", "mkuzzm", "Score 100K", 100000),
        ("event_callback_nyi04s", "nyi04s", "Score 250K", 250000),
        ("event_callback_1v45em", "1v45em", "Score 500K", 500000),
        ("event_callback_q3tfto", "q3tfto", "Score 750K", 750000),
        ("event_callback_o9d9hb", "o9d9hb", "Score 1M", 1000000),
    ])

    # Bravo Slots
    add_list("bravo_slots", [
        ("event_callback_pxnk4e", "pxnk4e", "Reach Level 40", 40),
        ("event_callback_k6p17i", "k6p17i", "Reach Level 100", 100),
        ("event_callback_fw0837", "fw0837", "Purchase Mission Pass", 0),
        ("event_callback_i1l8xp", "i1l8xp", "Reach Level 200", 200),
        ("event_callback_nlql3m", "nlql3m", "Reach Level 400", 400),
        ("event_callback_1pvoa2", "1pvoa2", "Accum Purchase $9.99", 0),
        ("event_callback_96j1vw", "96j1vw", "Reach Level 800", 800),
        ("event_callback_jpw7pe", "jpw7pe", "Level 2000", 2000),
        ("event_callback_y85bjt", "y85bjt", "Level 4000", 4000),
    ])

    # Cash Storm
    add_list("cash_storm", [
        ("event_callback_ht80ad", "ht80ad", "Complete Level 15", 15),
        ("event_callback_ll59t0", "ll59t0", "Purchase any $9.99", 0),
        ("event_callback_47akr5", "47akr5", "Level 30", 30),
        ("event_callback_yjd7i0", "yjd7i0", "Level 40", 40),
        ("event_callback_fmwgmq", "fmwgmq", "Level 60", 60),
        ("event_callback_6nulf0", "6nulf0", "Purchase any $19.9", 0),
        ("event_callback_6ppgib", "6ppgib", "Level 80", 80),
        ("event_callback_qyasgc", "qyasgc", "Level 100", 100),
    ])

    # Climb Mountain
    add_list("climb_mountain", [
        ("event_callback_xt4epl", "xt4epl", "Complete Level 25", 25),
        ("event_callback_n2qh1u", "n2qh1u", "Level 100", 100),
        ("event_callback_bssey9", "bssey9", "Level 300", 300),
    ])

    # Clock Maker
    add_list("clock_maker", [
        ("event_callback_uu8lcy", "uu8lcy", "Unlock Stables", 1),
        ("event_callback_64yi1x", "64yi1x", "Unlock the Mill", 2),
        ("event_callback_gwqs4i", "gwqs4i", "Unlock Old Sam's House", 3),
        ("event_callback_uqry54", "uqry54", "Unlock Harrison's Mansion", 4),
        ("event_callback_1nwuqr", "1nwuqr", "Unlock Fire Station", 5),
        ("event_callback_as93wo", "as93wo", "Unlock Antique Shop", 6),
        ("event_callback_86t122", "86t122", "Unlock Theatre", 7),
        ("event_callback_t912za", "t912za", "Unlock School", 8),
        ("event_callback_senibm", "senibm", "Unlock Fountain", 9),
        ("event_callback_g8g4p2", "g8g4p2", "Unlock the Clock Tower", 10),
        ("event_callback_bev80p", "bev80p", "Purchase", 0),
    ])


add_adj_events()

conn.commit()

# ==================== Seed Admin Users ====================
from datetime import datetime
now = datetime.now().isoformat()

cur.execute(
    "INSERT INTO users (user_id, username, name, admin, allowed, created_at) VALUES (%s, %s, %s, %s, %s, %s) "
    "ON CONFLICT (user_id) DO NOTHING",
    (6075014046, "admin", "Admin", 1, 1, now),
)
cur.execute(
    "INSERT INTO allowed_users (user_id, username, name, added_by, added_date) VALUES (%s, %s, %s, %s, %s) "
    "ON CONFLICT (user_id) DO NOTHING",
    (6075014046, "admin", "Admin", 6075014046, now),
)
cur.execute(
    "INSERT INTO users (user_id, username, name, admin, allowed, created_at) VALUES (%s, %s, %s, %s, %s, %s) "
    "ON CONFLICT (user_id) DO NOTHING",
    (8114043468, "admin2", "Admin2", 1, 1, now),
)
cur.execute(
    "INSERT INTO allowed_users (user_id, username, name, added_by, added_date) VALUES (%s, %s, %s, %s, %s) "
    "ON CONFLICT (user_id) DO NOTHING",
    (8114043468, "admin2", "Admin2", 6075014046, now),
)
cur.execute(
    "INSERT INTO user_platform (user_id, platform) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING",
    (6075014046, "android"),
)
cur.execute(
    "INSERT INTO user_platform (user_id, platform) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING",
    (8114043468, "android"),
)

conn.commit()

# ==================== Summary ====================
cur.execute("SELECT COUNT(*) FROM games_af")
af_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM games_singular")
sg_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM games_adj")
adj_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM events_af")
ev_af = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM events_singular")
ev_sg = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM events_adj")
ev_adj = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM users")
users_count = cur.fetchone()[0]

print(f"Seed complete:")
print(f"  AF games: {af_count}, events: {ev_af}")
print(f"  Singular games: {sg_count}, events: {ev_sg}")
print(f"  Adjust games: {adj_count}, events: {ev_adj}")
print(f"  Users: {users_count}")

cur.close()
conn.close()
