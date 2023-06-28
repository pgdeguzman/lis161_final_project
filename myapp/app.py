from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from data import *
from functools import wraps
from werkzeug.utils import secure_filename

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

@app.route('/faq')
def faq():
    return render_template('faq.html')

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
    return render_template("item.html", name=name, size=size, item=item, product=item, description=description, stock=stock, price=price, image_path=image_path)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        size = request.form['size']
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files['image']
        stock = request.form['stock']
        
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.root_path, 'static/img', image_filename)
        image_file.save(image_path)
        
        insert_item_into_db(name, size, price, description, image_filename, stock)
        
        flash('Item added successfully!')
        
        return redirect('/register')

    return render_template('register.html')

@app.route('/processed', methods=['POST'])
@login_required
def processing():
    return redirect(url_for('products'))

@app.route('/modify', methods=['POST'])
@login_required
def modify():
    action = request.form["action"]
    product_id = request.form["product_id"]
    if action == "edit":
        item = get_item_by_id(product_id)
        return render_template('update.html', item=item)
    elif action == "delete":
        delete_item({'product_id': product_id})
        return redirect(url_for('products'))


@app.route('/update', methods=['POST'])
@login_required
def update():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    price = request.form.get('price')
    size = request.form.get('size')
    description = request.form.get('description')
    stock = request.form.get('stock')
    image_file = request.files.get('image_filename')

    if image_file:
        image_filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    else:
        image_filename = None

    product_data = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "size": size,
        "description": description,
        "stock": stock,
        "image_filename": image_filename
    }
    
    if 'image' not in product_data:
        product_data['image'] = None

    update_item(product_data)
    return redirect(url_for('item', name=name))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    return render_template('buy.html')

@app.route('/purchase_success')
def purchase_success():
    return render_template('purchase_success.html')

if __name__ == "__main__":
    app.run(debug=True)