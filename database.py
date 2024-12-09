import sqlite3

def get_db_connection():
    conn = sqlite3.connect('Data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_name TEXT NOT NULL,
        description TEXT,
        available BOOLEAN NOT NULL,
        quantity INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        allergen_name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS customer_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suggestion TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        flavor_id INTEGER,
        quantity INTEGER
    )''')

    conn.commit()
    conn.close()

def add_flavor(flavor_name, description, available, quantity):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO seasonal_flavors (flavor_name, description, available, quantity) VALUES (?, ?, ?, ?)',
        (flavor_name, description, available, quantity)
    )
    conn.commit()
    conn.close()

def get_seasonal_flavors():
    conn = get_db_connection()
    flavors = conn.execute('SELECT * FROM seasonal_flavors').fetchall()
    conn.close()
    return flavors

def add_ingredient(ingredient_name):
    conn = get_db_connection()
    conn.execute('INSERT INTO ingredients (ingredient_name) VALUES (?)', (ingredient_name,))
    conn.commit()
    conn.close()

def get_ingredients():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    conn.close()
    return ingredients

def add_customer_suggestion(suggestion):
    conn = get_db_connection()
    conn.execute('INSERT INTO customer_suggestions (suggestion) VALUES (?)', (suggestion,))
    conn.commit()
    conn.close()

def get_customer_suggestions():
    conn = get_db_connection()
    suggestions = conn.execute('SELECT * FROM customer_suggestions').fetchall()
    conn.close()
    return suggestions

def add_allergen(allergen_name):
    conn = get_db_connection()
    conn.execute('INSERT INTO allergens (allergen_name) VALUES (?)', (allergen_name,))
    conn.commit()
    conn.close()

def get_allergens():
    conn = get_db_connection()
    allergens = conn.execute('SELECT * FROM allergens').fetchall()
    conn.close()
    return allergens

def add_to_cart(user_id, flavor_id, quantity):
    conn = get_db_connection()
    existing_item = conn.execute('SELECT * FROM cart WHERE user_id = ? AND flavor_id = ?', (user_id, flavor_id)).fetchone()
    if existing_item:
        conn.execute(
            'UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND flavor_id = ?', (quantity, user_id, flavor_id)
        )
    else:
        conn.execute(
            'INSERT INTO cart (user_id, flavor_id, quantity) VALUES (?, ?, ?)', (user_id, flavor_id, quantity)
        )
    conn.commit()
    conn.close()

def get_user_cart(user_id):
    conn = get_db_connection()
    cart_items = conn.execute('''SELECT cart.id, cart.quantity, seasonal_flavors.flavor_name, cart.flavor_id FROM cart JOIN seasonal_flavors ON cart.flavor_id = seasonal_flavors.id WHERE cart.user_id = ?''', (user_id,)).fetchall()
    conn.close()
    return cart_items

def remove_from_cart(user_id, cart_item_id, quantity):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_item_id, user_id))
    conn.commit()
    conn.close()

def update_flavor_quantity(flavor_id, quantity):
    conn = get_db_connection()
    conn.execute(
        'UPDATE seasonal_flavors SET quantity = quantity + ? WHERE id = ?', (quantity, flavor_id)
    )
    conn.commit()
    conn.close()

def get_cart_item_by_id(cart_item_id):
    conn = get_db_connection()
    cart_item = conn.execute('SELECT * FROM cart WHERE id = ?', (cart_item_id,)).fetchone()
    conn.close()
    return cart_item

def search_flavors(search_query):
    conn = get_db_connection()
    query = f"%{search_query}%"
    flavors = conn.execute('''SELECT * FROM seasonal_flavors WHERE flavor_name LIKE ? OR description LIKE ?''', (query, query)).fetchall()
    conn.close()
    return flavors

def allergen_exists(allergen_name):
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM allergens WHERE allergen_name = ?', (allergen_name,)).fetchone()
    conn.close()
    return result is not None

def add_customer_suggestion(suggestion):
    conn = get_db_connection()
    conn.execute('INSERT INTO customer_suggestions (suggestion) VALUES (?)', (suggestion,))
    conn.commit()
    conn.close()

def get_customer_suggestions():
    conn = get_db_connection()
    suggestions = conn.execute('SELECT * FROM customer_suggestions').fetchall()
    conn.close()
    return suggestions

def delete_flavor_by_id(flavor_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM seasonal_flavors WHERE id = ?', (flavor_id,))
    conn.commit()
    conn.close()