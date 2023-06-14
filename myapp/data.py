import sqlite3

db_path = "pa.db"

def connect_to_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

def read_pets_by_pet_type(pet_type):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM pets WHERE animal_type = ?'
    value = pet_type
    results = cur.execute(query,(value,)).fetchall()
    conn.close()
    return results

def read_pet_by_pet_id(pet_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM pets WHERE id = ?'
    value = pet_id
    result = cur.execute(query,(value,)).fetchone()
    conn.close()
    return result

def insert_pet(pet_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO pets (animal_type, name, age, breed, description, url) VALUES (?,?,?,?,?,?)'
    values = (pet_data['pet_type'], pet_data['name'],
              pet_data['age'], pet_data['breed'],
              pet_data['description'], pet_data['url'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

def update_pet(pet_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE pets SET animal_type=?, name=?, age=?, breed=?, description=?, url=? WHERE id=?"
    values = (pet_data['pet_type'],
              pet_data['name'],
              pet_data['age'],
              pet_data['breed'],
              pet_data['description'],
              pet_data['url'],
              pet_data['pet_id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def delete_pet(pet_data):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM pets WHERE id=?"
    values = (pet_data['pet_id'], )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def perform_search(query, criteria):
    conn, cur = connect_to_db(db_path)

    if criteria == "animal_type":
        column_name = "animal_type"
    elif criteria == "breed":
        column_name = "breed"
    elif criteria == "name":
        column_name = "name"
    elif criteria == "age":
        column_name = "age"
    else:
        column_name = None

    if column_name:
        search_query = f"%{query}%"
        cur.execute(f"SELECT * FROM pets WHERE {column_name} LIKE ?", (search_query,))
        search_results = [dict(row) for row in cur.fetchall()]
    else:
        search_results = []

    conn.close()
    return search_results