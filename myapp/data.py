import sqlite3

db_path = "pa.db"

# This function conencts to the DB and returns a conn and cur objects
def connect_to_db(path):
    conn = sqlite3.connect(path)
    # Converting tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# This function returns pets by pet_type
def read_pets_by_pet_type(pet_type):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM pets WHERE animal_type = ?'
    value = pet_type
    results = cur.execute(query,(value,)).fetchall()
    conn.close()
    return results

# This function retrieves 1 pet by pet_id
def read_pet_by_pet_id(pet_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM pets WHERE id = ?'
    value = pet_id
    result = cur.execute(query,(value,)).fetchone()
    conn.close()
    return result

# This function inserts 1 pet data
def insert_pet(pet_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO pets (animal_type, name, age, breed, description, url) VALUES (?,?,?,?,?,?)'
    values = (pet_data['pet_type'], pet_data['name'],
              pet_data['age'], pet_data['breed'],
              pet_data['description'], pet_data['url'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

# This function updates a record
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

# This function deletes the record
def delete_pet(pet_data):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM pets WHERE id=?"
    values = (pet_data['pet_id'], )
    cur.execute(query, values)
    conn.commit()
    conn.close()