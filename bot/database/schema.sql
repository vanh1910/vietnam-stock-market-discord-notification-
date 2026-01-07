CREATE TABLE IF NOT EXISTS "warns" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" VARCHAR(20) NOT NULL,
    "server_id" VARCHAR(20) NOT NULL,
    "moderator_id" VARCHAR(20) NOT NULL,
    "reason" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "tickers_users" (
    "user_id" INTEGER NOT NULL,
    "ticker" VARCHAR(3) NOT NULL,
    "server_id" VARCHAR(20),
    PRIMARY KEY ("user_id", "ticker"),
    FOREIGN KEY ("ticker") REFERENCES "tickers"("ticker")
);

CREATE TABLE IF NOT EXISTS "tickers" (
    "ticker" VARCHAR(3) NOT NULL,
    "timestamp" TIMESTAMP NOT NULL,
    "resolution" VARCHAR(2) NOT NULL,
    "high" INTEGER,
    "low" INTEGER,
    "open" INTEGER,
    "close" INTEGER,
    "volume" INTEGER,
    PRIMARY KEY ("ticker", "timestamp", "resolution")
);

CREATE TABLE IF NOT EXISTS "signals" (
    "signal_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "type" VARCHAR(10) NOT NULL,
    "value" INTEGER
);

CREATE TABLE IF NOT EXISTS "cp_channel"(
    "channel_id" INTEGER,
    PRIMARY KEY ("channel_id")
);
CREATE TABLE IF NOT EXISTS "cp_acc"(
    "user_id" INTEGER,
    "handle" VARCHAR(20),
    "platform" VARCHAR(6),
    PRIMARY KEY ("user_id", "platform")
);

CREATE TABLE IF NOT EXISTS "user_cp_streak"(
    "user_id" INTEGER,
    "channel_id" INTEGER,
    "streak" INTEGER,
    "last_submit" INTEGER,
    "solved_problems" INTEGER,
    PRIMARY KEY ("user_id")
);

CREATE TABLE IF NOT EXISTS "daily_problem"(
    "date" INTEGER,
    "problem_id" VARCHAR(10),
    "platform" VARCHAR(6)
);