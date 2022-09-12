from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user_model import User


@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/recipes')
    return render_template('index.html')




'''
*******************ACTTION ROUTES********************
'''


@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name":request.form['fname'],
        "last_name":request.form['lname'], 
        "password":pw_hash,
        "email":request.form['email'] 
    }
    user_id = User.add(data)
    session['uuid'] = user_id
    return redirect('/recipes')

@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    return redirect('/recipes')


@app.route("/logout")
def logout():
    if 'uuid' not in session:
        return redirect('/')
    del session['uuid']
    # del session['username']
    return redirect('/')

