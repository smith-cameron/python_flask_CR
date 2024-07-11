from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def index():
  
  return render_template('index.html') 


@app.route('/users/create', methods=['POST'])
def users_create():
    print(f"request.form: {request.form}") 
    # Send the request.form to the model -> database
    # inserting that form data as a new row in the users table
    user_data ={
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'email': request.form['email'],
      'password': request.form['password'],
    }
    user_id = User.create(user_data)
    # redirect to '/dash'
    return redirect(f'/dash/{user_id}')  

@app.route('/dash/<int:user_id>')
def dashboard(user_id):
  print(f"dash user_id: {user_id}")
  
  return render_template('dashboard.html', current_user = User.get_one({'id' : user_id}))

@app.route('/logout')
def clear_session():
    session.clear()

    return redirect('/') 