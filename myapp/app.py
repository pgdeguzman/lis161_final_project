from flask import Flask, render_template, request, redirect, url_for, session
import os
from data import *
from functools import wraps

app = Flask(__name__)

app.secret_key = 'cosmo_apparel_secret_key'

picFolder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
@app.route('/home')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'shirt-1.jpg')
    shirts = []
    unique_images = set()
    for item in get_all_items():
        image_url = item['image_url']
        if image_url not in unique_images:
            shirts.append(image_url)
            unique_images.add(image_url)
            if len(shirts) == 3:
                break
    return render_template('index.html', user_image_=pic1, shirts=shirts)

def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)

app.jinja_env.filters['enumerate'] = jinja2_enumerate

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_answer = request.form.get('security_answer')

        if user_answer == 'itsme':
            session['logged_in'] = True
            return redirect(url_for('register'))
        else:
            error_message = 'Incorrect answer'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    item_list = get_all_items()
    return render_template("products.html", items=item_list)

@app.route('/products/<string:name>')
def item(name):
    size = request.args.get('size', default=None)
    item = get_item_by_name(name)
    description = get_description_by_name_and_size(name, size)
    stock = get_stock_by_name_and_size(name, size)
    price = get_price_by_name_and_size(name, size)
    image_filename = item['image_url']
    image_path = url_for('static', filename='img/' + image_filename)
    return render_template("item.html", name=name, size=size, item=item, description=description, stock=stock, price=price, image_path=image_path)

@app.route('/register')
@login_required
def register():
    return render_template('register.html')

@app.route('/processed', methods=['POST'])
@login_required
def processing():
    product_data = {
        "name": request.form['p_name'],
        "price": request.form['p_price'],
        "sizes": {
            request.form['p_size']: request.form['p_price']
        },
        "image": request.form['p_url'],
        "description": request.form['p_desc'],
        "stock": {
            request.form['p_size']: 10
        },
        "timestamp": "Some timestamp"
    }
    insert_item(product_data)
    return redirect(url_for('products'))

@app.route('/modify', methods=['POST'])
@login_required
def modify():
    if request.form["modify"] == "edit":
        product_id = request.form["product_id"] 
        item = get_item_by_id(product_id)
        return render_template('update.html', item=item)
    elif request.form["modify"] == "delete":
        product_id = request.form["product_id"]
        item = get_item_by_id(product_id)
        delete_item({'product_id': product_id})
        return redirect(url_for('products'))

@app.route('/update', methods=['POST'])
@login_required
def update():
    product_data = {
        "product_id": request.form['product_id'],
        "name": request.form['p_name'],
        "price": request.form['p_price'],
        "sizes": {
            request.form['p_size']: request.form['p_price']
        },
        "image": request.form['p_url'],
        "description": request.form['p_desc'],
    }
    update_item(product_data)
    return redirect(url_for('item', name=request.form['p_name']))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        address = request.form.get('address')
        quantity = request.form.get('quantity')
        item_name = request.args.get('name')
        item = get_item_by_name(item_name)

        if not name or not contact or not address or not quantity:
            session['error_message'] = 'Please fill in all the required fields.'
            return redirect(url_for('buy', name=item_name))

        if not item:
            session['error_message'] = 'Item not found.'
            return redirect(url_for('buy', name=item_name))

        if quantity and quantity.isdigit() and int(quantity) > 0 and int(quantity) <= item['stock']:
            quantity = int(quantity)
            # Process the purchase
            updated_stock = item['stock'] - quantity
            update_item_stock(item['id'], updated_stock)

            return redirect(url_for('purchase_success', item_name=name, quantity=quantity, buyer_name=name, contact_details=contact, address=address))
        else:
            session['error_message'] = 'Invalid quantity or desired quantity is higher than the currently available stock. Please re-enter.'
            return redirect(url_for('buy', name=item_name))
    else:
        item_name = request.args.get('name')
        item = get_item_by_name(item_name)

        if not item:
            session['error_message'] = 'Item not found.'
            return redirect(url_for('index'))

        return render_template('buy.html', product=item)

@app.route('/purchase_success')
def purchase_success():
    return render_template('purchase_success.html')

if __name__ == "__main__":
    app.run(debug=True)