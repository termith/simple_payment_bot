CREATE TABLE IF NOT EXISTS chats
(
    chat_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_chat_id TEXT,
    chat_settings TEXT
);

CREATE TABLE IF NOT EXISTS payments
(
    payment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id      INTEGER,
    payment_date TEXT,
    FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
);

