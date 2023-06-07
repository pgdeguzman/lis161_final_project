from flask import Flask, render_template, request, redirect, url_for
from data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/animals/<pet_type>')
def animals(pet_type):
    pets_list = read_pets_by_pet_type(pet_type)
    return render_template("animals.html", pet_type=pet_type, pets=pets_list)

@app.route('/animals/<int:pet_id>')
def pet(pet_id):
    pet = read_pet_by_pet_id(pet_id)
    return render_template("pet.html",pet=pet)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processed', methods=['post'])
def processing():
    pet_data = {
        "pet_type": request.form['pet_type'],
        "name": request.form['pet_name'],
        "breed": request.form['pet_breed'],
        "age": request.form['pet_age'],
        "description": request.form['pet_desc'],
        "url": request.form['pet_url']
    }
    insert_pet(pet_data)
    return redirect(url_for('animals', pet_type=request.form['pet_type']))


@app.route('/modify', methods=['post'])
def modify():
    # 1. identify whether user clicked edit or delete
       # if edit, then do this:
    if request.form["modify"] == "edit":
        # retrieve record using id
        pet_id = request.form["pet_id"] 
        pet = read_pet_by_pet_id(pet_id)
        # update record with new data
        return render_template('update.html', pet=pet)
    # if delete, then do this
    elif request.form["modify"] == "delete":
        # retrieve record using id
        # delete the record
        # redirect user to pet list by pet type
        pass

@app.route('/update', methods=['post'])
def update():
    pet_data = {
        "pet_id" : request.form["pet_id"],
        "pet_type": request.form['pet_type'],
        "name": request.form['pet_name'],
        "breed": request.form['pet_breed'],
        "age": request.form['pet_age'],
        "description": request.form['pet_desc'],
        "url": request.form['pet_url']
    }
    update_pet(pet_data)
    return redirect(url_for('pet',pet_id = request.form['pet_id']))

if __name__ == "__main__":
    app.run(debug=True)