
## Connecting to a Database([[mysqlDB.py]])
[Connecting to a Database- Platform](https://login.codingdojo.com/m/506/12463/87417)
MAIN POINTS
- Of `import pymysql.cursors` cursor is the pymysql package object we use to interact with the database
- `class MySQLConnection` will give us an __instance__ of a connection to our database
- [ ] Change the connection info to reflect your local settings for mysql
- Db is a parameter and will be defined when you call on the class
==“try - catch” is used when you know a block of code may possible fail and success/error is dependent on outside information==
- `SELECT` queries will return a list of dictionaries via return `cursor.fetchall()`
- `INSERT` queries will return the auto-generated id of the inserted row return `cursor.lastrowid`
- `UPDATE` and `DELETE` queries will return nothing
	- If you want them to return something this is where you can change it
	- If you want to use another mysql query it will work but won't return anything. To return something it will have to be defined or the `else` catches it.
- If the query goes wrong, it will return False
```python
except Exception as e:
	# if the query fails the method will return FALSE
	print("Something went wrong", e)
	return False
```


Specifically `"Something went wrong", mysql_error_returned` ==Look for this in your terminal==
`def connect(db):` Returns an instance if the `MySQLConnection` and will be the method you call from your models to run queries.


---
## Model - user.py
- [ ] Create user.py file
- [ ] `from mysqlDB import connect` To import connection class
- [ ] Define your schema name either globally or as a class variable
- [ ] model the class after the users table from our database
	- This reflects the dictionary keys will be structured upon query return
```python
from flask_app.config.mysqlDB import connect

class User:
	mydb = 'schemaName'
	def __init__(self, data):
		self.id = data['id']
		self.first_name = data['first_name']
		self.last_name = data['last_name']
		self.email = data['email']
		self.password = data['password']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
```
This `__init__` method will take in self (of course) and a variable to carry a dictionary that is being returned from mysql connection file
### [[Model - @classmethod]]
use `@classmethod` to query our database, __WHY__?
*You can use class methods for any methods that are not bound to a specific instance but the class. In practice, you often use class methods for methods that create an instance of the class. When a method creates an instance of the class and returns it, the method is called a factory method.*

- [ ] Multi-line strings will help debug faster with more complicated queries that have more variables
- [ ] call the `connect()` function with arguments
	- [ ] the *schema* you are targeting
	- [ ] the *query* you wish to run
	`dbReturnList = connectToMySQL(schema variable).query_db(query)`
[Queries with Variable Data - Platform](https://login.codingdojo.com/m/506/12464/87420)
#### CREATE
We are passing variable placeholders where the keys are the same as the “name” in the form and match request.form
OR alternatively the key of a dictionary we create ourselves
__templates/form.html__
```html
 <h3>Create a User</h3>
    <form action="/users" method="post">
      <label for="first_name">First Name:</label>
      <input type="text" name="first_name" />
      <label for="last_name">Last Name:</label>
      <input type="text" name="last_name" />
      <label for="email">Email:</label>
      <input type="email" name="email" />
      <label for="password">Password:</label>
      <input type="password" name="password" />
      <!-- <input type="submit" value="create user" /> -->
      <button>Submit Form</button>
    </form>
```
__controllers/user_controller.py__
```python
@app.route('/users', methods=['post'])
def form_post_rout():
	print(f"POST route: {request.form}")
	data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password" : request.form["password"]
    }
	user_id = User.save(data)
	session['userId'] = user_id
	return redirect('/')
```
__models/user.py__
```python
@classmethod
def save(cls, data):
	query = '''
	INSERT INTO users 
	(first_name, last_name, email, password)
	VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
	'''
	# results = connectToMySQL(mydb).query_db(query, data)
	# print(results)
	return connect(cls.myDB).query_db(query, data)
```
#### Get One
__templates/form.html__
```html
<td><a href="/users/show/{{user.id}}">{{user.first_name}}</a></td>
```
__controllers/user_controller.py__
```python
@app.route('/users/show/<int:user_id>')
def render_post(user_id):
    print(f"user id to Show: {user_id}")
    this_user= User.get_by_id({'id': user_id})
    return render_template('displayOne.html',user = this_user)
```
__models/user.py__
```python
@classmethod
    def get_by_id(cls, data):
        print(f"data variable: {data}")
        query = '''
        SELECT *
        FROM users
        WHERE id = %(id)s;'''
        this_user = connectToMySQL(cls.myDB).query_db(query, data)
        #print(f"debugging: {cls(this_user[0])}")
        return cls(this_user[0])
```
