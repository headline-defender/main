import sqlite3

# 定点の情報を登録
def create_lineups(cursor, map_name, agent_name, site_name, effect_type):
    try:
        cursor.execute("""
        INSERT INTO lineups (map_name, agent_name, site, effect_type)
        VALUES (?, ?, ?, ?)
        """, (map_name, agent_name, site_name, effect_type))
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False

def create_point(cursor, lineup_id, marker_x, marker_y):
    try:
        cursor.execute("""
        INSERT INTO lineup_point_effects (lineup_id, x, y)
        VALUES (?, ?, ?)
        """, (lineup_id, marker_x, marker_y))
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False

def create_vector(cursor, lineup_id, start_x, start_y, end_x, end_y):
    try:
        cursor.execute("""
        INSERT INTO lineup_vector_effects (lineup_id, start_x, start_y, end_x, end_y)
        VALUES (?, ?, ?, ?, ?)
        """, (lineup_id, start_x, start_y, end_x, end_y))
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False
    
def create_lineup_images(cursor, lineup_id, filepath, description, is_position = 0):
    try:
        cursor.execute("""
            INSERT INTO lineup_images (lineup_id, is_position, image_path, description)
            VALUES (?, ?, ?, ?)
        """, (lineup_id, is_position, filepath, description))
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False
    
def read_lineups(cursor, map_name, agent_name):
    try:
        cursor.execute("""
            SELECT * FROM lineups WHERE map_name = ? and agent_name = ?
        """, (map_name, agent_name))
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False

# lineup_id_listで指定したidの情報を取得する
def read_lineup_image(cursor, lineup_id_list):
    placeholders = ','.join('?' for _ in lineup_id_list)
    try:
        sql = f"SELECT lineup_id, image_path, description FROM lineup_images WHERE lineup_id IN ({placeholders})"
        cursor.execute(sql, lineup_id_list)
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False

# lineup_id_listで指定したidのポイント情報を取得する
def read_point_effects(cursor, lineup_id_list):
    placeholders = ','.join('?' for _ in lineup_id_list)
    try:
        sql = f"SELECT lineup_id, x, y FROM lineup_point_effects WHERE lineup_id IN ({placeholders})"
        cursor.execute(sql, lineup_id_list)
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False

# lineup_id_listで指定したidのベクトル情報を取得する
def read_vector_effects(cursor, lineup_id_list):
    placeholders = ','.join('?' for _ in lineup_id_list)
    try:
        sql = f"SELECT lineup_id, start_x, start_y, end_x, end_y FROM lineup_vector_effects WHERE lineup_id IN ({placeholders})"
        cursor.execute(sql, lineup_id_list)
        return True
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        return False