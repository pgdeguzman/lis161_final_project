from flask import Flask, render_template, request, redirect, url_for, session
import os
from data import *
from functools import wraps

app = Flask(__name__)

app.secret_key = 'cosmo_apparel_secret_key'

picFolder = os.path.join('static','img')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
@app.route('/home')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'shirt-1.jpg')
    shirts = ['shirt-1.jpg', 'shirt-2.jpg', 'shirt-3.jpg', 'shirt-4.jpg', 'shirt-5.jpg', 'shirt-6.jpg']
    return render_template('index.html', user_image_=pic1, shirts=shirts) 

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

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products/<int:product_id>')
def pet(product_id):
    item = get_item_by_id(product_id)
    return render_template("item.html", item=item)

@app.route('/products/<product_type>')
def animals(product_type):
    item_list = get_all_items(product_type)
    return render_template("products.html", product_type=product_type, items=item_list)

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
        "size": request.form['p_size'],
        "image": request.form['p_url'],
        "desc": request.form['p_desc'],
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
        "size": request.form['p_size'],
        "image": request.form['p_url'],
        "desc": request.form['p_desc'],
    }
    update_item(product_data)
    return redirect(url_for('item', product_id=request.form['product_id']))

@app.route('/search')
def search():
    query = request.args.get('query')
    criteria = request.args.get('criteria')
    search_results = perform_search(query, criteria)
    return render_template('search.html', query=query, criteria=criteria, results=search_results)

if __name__ == "__main__":
    app.run(debug=True)
