CREATE TABLE lineups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    map_name TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    site TEXT,
    effect_type TEXT NOT NULL CHECK (effect_type IN ('point', 'vector')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lineup_point_effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lineup_id INTEGER NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lineup_id) REFERENCES lineups(id) ON DELETE CASCADE
);

CREATE TABLE lineup_vector_effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lineup_id INTEGER NOT NULL,
    start_x REAL NOT NULL,
    start_y REAL NOT NULL,
    end_x REAL NOT NULL,
    end_y REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lineup_id) REFERENCES lineups(id) ON DELETE CASCADE
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
