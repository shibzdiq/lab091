from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Завантаження конфігурації
load_dotenv()
app = Flask(__name__)

# Підключення до MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["car_catalog"]

# Колекції
cars_collection = db["cars"]
specs_collection = db["specs"]
users_collection = db["users"]

# Головна сторінка
@app.route('/')
def index():
    cars = list(cars_collection.find())
    specs = list(specs_collection.find())
    users = list(users_collection.find())
    return render_template('index.html', cars=cars, specs=specs, users=users)


# CRUD для автомобілів
@app.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year'])
        }
        cars_collection.insert_one(car)
        return redirect(url_for('index'))
    return render_template('car_form.html', car=None)

@app.route('/cars/edit/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = cars_collection.find_one({"_id": ObjectId(car_id)})
    if request.method == 'POST':
        updated_car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year'])
        }
        cars_collection.update_one({"_id": ObjectId(car_id)}, {"$set": updated_car})
        return redirect(url_for('index'))
    return render_template('car_form.html', car=car)

@app.route('/cars/delete/<car_id>')
def delete_car(car_id):
    cars_collection.delete_one({"_id": ObjectId(car_id)})
    return redirect(url_for('index'))

# CRUD для характеристик
@app.route('/specs/add', methods=['GET', 'POST'])
def add_spec():
    if request.method == 'POST':
        spec = {
            "engine": request.form['engine'],
            "horsepower": int(request.form['horsepower']),
            "fuel_type": request.form['fuel_type']
        }
        specs_collection.insert_one(spec)
        return redirect(url_for('index'))
    return render_template('spec_form.html', spec=None)

@app.route('/specs/edit/<spec_id>', methods=['GET', 'POST'])
def edit_spec(spec_id):
    spec = specs_collection.find_one({"_id": ObjectId(spec_id)})
    if request.method == 'POST':
        updated_spec = {
            "engine": request.form['engine'],
            "horsepower": int(request.form['horsepower']),
            "fuel_type": request.form['fuel_type']
        }
        specs_collection.update_one({"_id": ObjectId(spec_id)}, {"$set": updated_spec})
        return redirect(url_for('index'))
    return render_template('spec_form.html', spec=spec)

@app.route('/specs/delete/<spec_id>')
def delete_spec(spec_id):
    specs_collection.delete_one({"_id": ObjectId(spec_id)})
    return redirect(url_for('index'))

# CRUD для користувачів
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password']
        }
        users_collection.insert_one(user)
        return redirect(url_for('index'))
    return render_template('user_form.html', user=None)

@app.route('/users/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if request.method == 'POST':
        updated_user = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password']
        }
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
        return redirect(url_for('index'))
    return render_template('user_form.html', user=user)

@app.route('/users/delete/<user_id>')
def delete_user(user_id):
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
