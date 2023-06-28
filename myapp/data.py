import sqlite3

db_path = "items.db"

def connect_to_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def get_item_by_name(name):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT *, "/static/img/" || image_filename AS image_url FROM items WHERE name = ?'
    value = name
    result = cur.execute(query, (value,)).fetchone()
    conn.close()
    return result

def get_all_items():
    conn, cur = connect_to_db(db_path)
    query = 'SELECT *, "/static/img/" || image_filename AS image_url FROM items'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

def get_item_by_id(product_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT *, "/static/img/" || image_filename AS image_url FROM items WHERE id = ?'
    value = product_id
    result = cur.execute(query, (value,)).fetchone()
    conn.close()
    return result

def insert_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO items (name, price, size, image_filename, description, stock) VALUES (?, ?, ?, ?, ?, ?)'
    values = (
        product_data['name'],
        product_data['price'],
        product_data['size'],
        product_data['image_filename'],
        product_data['description'],
        product_data['stock']
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE items SET name=?, price=?, size=?, image_filename=?, description=? WHERE id=?"
    values = (
        product_data['name'],
        product_data['price'],
        product_data['size'],
        product_data['image_filename'],
        product_data['description'],
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

def update_item_stock(item_id, new_stock):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE items SET stock = ? WHERE id = ?"
    values = (new_stock, item_id)
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_stock(name, stock):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE items SET stock = ? WHERE name = ?"
    values = (stock, name)
    cur.execute(query, values)
    conn.commit()
    conn.close()

def check_stock(item_id, size):
    conn, cur = connect_to_db(db_path)
    query = "SELECT stock FROM items WHERE id=? AND size=?"
    values = (item_id, size)
    result = cur.execute(query, values).fetchone()
    conn.close()
    return result[0] if result else 0

def insert_item_into_db(name, size, price, description, image_filename, stock):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO items (name, size, price, description, image_filename, stock) VALUES (?, ?, ?, ?, ?, ?)'
    values = (name, size, price, description, image_filename, stock)
    cur.execute(query, values)
    conn.commit()
    conn.close()

def get_sizes_by_name(name):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT id, size FROM items WHERE name = ?'
    value = name
    results = cur.execute(query, (value,)).fetchall()
    conn.close()
    return [{'id': result['id'], 'size': result['size']} for result in results]

def create_purchase(purchase_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO purchases (product_name, size, price, your_name, contact_details, address, proof_of_payment) VALUES (?, ?, ?, ?, ?, ?, ?)'
    values = (
        purchase_data['product_name'],
        purchase_data['size'],
        purchase_data['price'],
        purchase_data['your_name'],
        purchase_data['contact_details'],
        purchase_data['address'],
        purchase_data['proof_of_payment']
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def get_all_purchases():
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM purchases'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

def decrease_stock(item_id, size):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE items SET stock = stock - 1 WHERE id = ? AND size = ?"
    values = (item_id, size)
    cur.execute(query, values)
    conn.commit()
    conn.close()
