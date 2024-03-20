from flask import Flask, redirect, request, jsonify, render_template, url_for
import pymysql.cursors

# Flask application instance
app = Flask(__name__)

# Database connection configuration
def db_connection():
    return pymysql.connect(host='localhost',
                           user='root',  # replace with your MySQL username
                           password='manoj123',  # replace with your MySQL password
                           db='inventory_management',
                           cursorclass=pymysql.cursors.DictCursor)

# Test route to ensure app is working
# @app.route('/')
#def home():
#    return 'Inventory Management System is online!'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/items', methods=['POST'])
def create_item():
    conn = db_connection()
    cursor = conn.cursor()
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    sql = "INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, quantity, price))
    conn.commit()
    return jsonify({'status': 'Item added successfully'}), 201
@app.route('/items', methods=['GET'])
def read_items():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return jsonify(items), 200
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    conn = db_connection()
    cursor = conn.cursor()
    item = request.get_json()
    name = item['name']
    quantity = item['quantity']
    price = item['price']
    sql = """
    UPDATE items
    SET name=%s, quantity=%s, price=%s
    WHERE id=%s
    """
    cursor.execute(sql, (name, quantity, price, id))
    conn.commit()
    return jsonify({'status': 'Item updated successfully'}), 200
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM items WHERE id=%s"
    cursor.execute(sql, (id,))
    conn.commit()
    return jsonify({'status': 'Item deleted successfully'}), 200
@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        
        # Connect to the database
        conn = db_connection()
        cursor = conn.cursor()
        
        # SQL to insert the new item
        sql = "INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, quantity, price))
        conn.commit()  # Commit the transaction
        
        # Redirect to the view-items page to see the list of items
        return redirect(url_for('view_items.html'))
    else:
        # If it's a GET request, just render the add_item.html form
        return render_template('add_item.html')

@app.route('/view-items')
def view_items():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()  # Fetch all items from the database
    return render_template('view_items.html', items=items)
@app.route('/edit-item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Retrieve updated form data
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        
        # Update item in database
        sql = "UPDATE items SET name=%s, quantity=%s, price=%s WHERE id=%s"
        cursor.execute(sql, (name, quantity, price, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_items'))
    else:
        # Render edit_item.html with the current item data
        cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
        item = cursor.fetchone()
        conn.close()
        if item:
            return render_template('edit_item.html', item=item)
        else:
            return 'Item not found', 404


@app.route('/delete-item/<int:id>', methods=['POST'])
def delete_items(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_items'))


if __name__ == '__main__':
    app.run(debug=True)

