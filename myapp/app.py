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
    view = request.args.get('view', 'grid')
    item_list = get_all_items()
    return render_template("products.html", items=item_list, view=view)

@app.route('/products/<string:name>')
def item_by_name(name):
    item = get_sizes_by_name(name)
    product = get_item_by_name(name)
    return render_template("item.html", item=item, display_type='name', name=name, product=product)

@app.route('/products/<int:product_id>')
def item_by_id(product_id):
    item = get_item_by_id(product_id)
    image_filename = item['image_url']
    image_path = url_for('static', filename='img/' + image_filename)
    return render_template("item.html", item=item, display_type='id', product_id=product_id, product=item, image_path=image_path)

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
        
        insert_item(product_data={
            'name': name,
            'size': size,
            'price': price,
            'description': description,
            'image_filename': image_filename,
            'stock': stock
        })
        
        flash('Item added successfully!')
        
        return redirect(url_for('products'))

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
        delete_item(product_data={'product_id': product_id})
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
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_size = request.form['product_size']
        product_price = request.form['product_price']
        your_name = request.form.get('your_name')
        contact_details = request.form.get('contact_details')
        address = request.form.get('address')
        proof_of_payment = request.files.get('proof_of_payment')

        if not your_name or not contact_details or not address or not proof_of_payment:
            flash('Please fill in all required fields.')
            return redirect(request.url)

        proof_of_payment_filename = secure_filename(proof_of_payment.filename)
        image_path = os.path.join(app.root_path, 'static/img', proof_of_payment_filename)
        proof_of_payment.save(image_path)

        create_purchase(purchase_data={
            'product_name': product_name,
            'product_size': product_size,
            'product_price': product_price,
            'your_name': your_name,
            'contact_details': contact_details,
            'address': address,
            'proof_of_payment_filename': proof_of_payment_filename
        })

        flash('Item purchased successfully!')
        return redirect(url_for('purchase_success'))

    product_name = request.args.get('product_name')
    product_size = request.args.get('product_size') 
    product_price = request.args.get('product_price')
    return render_template('buy.html', product_name=product_name, product_size=product_size, product_price=product_price)

@app.route('/purchase_success', methods=['GET', 'POST'])
def purchase_success():
    purchase = get_all_purchases()
    return render_template('purchase_success.html', purchase=purchase)

if __name__ == "__main__":
    app.run(debug=True)