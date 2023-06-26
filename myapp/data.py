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
    query = 'SELECT * FROM items WHERE id = ?'
    value = product_id
    result = cur.execute(query, (value,)).fetchone()
    conn.close()
    return result

def get_description_by_name_and_size(name, size):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT description FROM items WHERE name = ? AND size = ?'
    values = (name, size)
    result = cur.execute(query, values).fetchone()
    conn.close()
    return result[0] if result else ""

def get_stock_by_name_and_size(name, size):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT stock FROM items WHERE name = ? AND size = ?'
    values = (name, size)
    result = cur.execute(query, values).fetchone()
    conn.close()
    return result[0] if result else 0

def get_price_by_name_and_size(name, size):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT price FROM items WHERE name = ? AND size = ?'
    values = (name, size)
    result = cur.execute(query, values).fetchone()
    conn.close()
    return result[0] if result else 0


def insert_item(product_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO items (name, price, size, image, description, stock, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)'
    values = (
        product_data['name'],
        product_data['price'],
        product_data['size'],
        product_data['image'],
        product_data['description'],
        product_data['stock'],
        product_data['timestamp']
    )
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

def create_purchase(product_name, size, quantity, price, your_name, contact_details, address, proof_of_payment):
    conn, cur = connect_to_db(db_path)
    query = "INSERT INTO purchased (Product_Name, Size, Quantity, Price, Your_Name, Contact_Details, Address, Proof_of_Payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        product_name,
        size,
        quantity,
        price,
        your_name,
        contact_details,
        address,
        proof_of_payment
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()