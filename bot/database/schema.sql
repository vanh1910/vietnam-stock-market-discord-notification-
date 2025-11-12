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
)