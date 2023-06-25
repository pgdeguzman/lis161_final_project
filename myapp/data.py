import sqlite3

db_path = "items.db"

def connect_to_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

#def get_all_items_by_type(product_type):
#    conn, cur = connect_to_db(db_path)
#    query = 'SELECT * FROM items WHERE product_type = ?'
#    value = product_type
#    results = cur.execute(query, (value,)).fetchall()
#    conn.close()
#    return results

def get_item_by_id(product_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT *, "/static/img/" || image_filename AS image_url FROM items WHERE id = ?'
    value = product_id
    result = cur.execute(query, (value,)).fetchone()
    conn.close()
    return result

def get_all_items():
    conn, cur = connect_to_db(db_path)
    query = 'SELECT *, "/static/img/" || image_filename AS image_url FROM items'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

def insert_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO items (name, price, size, image, image_filename, description) VALUES (?, ?, ?, ?, ?, ?)'
    values = (product_data['name'], product_data['price'], product_data['size'], product_data['image'], product_data['image_filename'], product_data['desc'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE items SET name=?, price=?, size=?, image=?, description=? WHERE id=?"
    values = (
        product_data['name'],
        product_data['price'],
        product_data['size'],
        product_data['image'],
        product_data['desc'],
        product_data['product_id'],
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def delete_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM items WHERE id=?"
    values = (product_data['product_id'],)
    cur.execute(query, values)
    conn.commit()
    conn.close()

def perform_search(query, criteria):
    conn, cur = connect_to_db(db_path)

    if criteria == "name":
        column_name = "name"
    elif criteria == "price":
        column_name = "price"
    else:
        column_name = None

    if column_name:
        search_query = f"%{query}%"
        cur.execute(f"SELECT * FROM items WHERE {column_name} LIKE ?", (search_query,))
        search_results = [dict(row) for row in cur.fetchall()]
    else:
        search_results = []

    conn.close()
    return search_results