CREATE TABLE lineups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    map_name TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    site TEXT,
    marker_x REAL NOT NULL,
    marker_y REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lineup_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lineup_id INTEGER NOT NULL,
    is_position INTEGER NOT NULL DEFAULT 0,
    image_path TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(lineup_id) REFERENCES lineups(id) ON DELETE CASCADE
);
