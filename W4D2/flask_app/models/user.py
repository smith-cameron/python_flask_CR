from flask_app.config.mysqlconnection import connect

class User:
  DB = 'flask_june_24'
  def __init__(self, data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def create(cls, form_data):
    print(f"model: {form_data}")
    query = """
    INSERT INTO users
    (first_name, last_name, email, password)
    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
    """
    user_id = connect(cls.DB).query_db(query, form_data)
    # print(user_id)
    return user_id

  @classmethod
  def get_one(cls, data):
    query = """
    SELECT * 
    FROM users
    WHERE id = %(id)s;
    """
    results = connect(cls.DB).query_db(query, data)
    print(results[0])
    return cls(results[0])