from flask import Flask, request, jsonify, abort
import pyodbc

app = Flask(__name__)
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')

#cursor = conn.cursor()
#cursor.execute("insert into madhav1 (id,name) values (14,'rav')")
#cursor.execute('SELECT * FROM madhav1')

# Configure MySQL connection
db_config = {'DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;'}

# User API

# Create a new user

@app.post('/add-item')
def add_item():
    user=request.get_json()
    if not user:
        return jsonify(message="Please provide data"), 400

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    # cursor.execute("insert into user_(userid,name,email,password) values ('1','Madha','36jhamadhav@gmail.com','123')")
    query = "INSERT INTO [user_] (userid, name, email, password) VALUES (?, ?, ?,?)"
    values = (user['id'],user['name'], user['email'], user['password'])
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(message="User created successfully"), 201
# Get a specific user
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    # query = "SELECT * FROM user_ WHERE userid = user_id"
    # values = (user_id)
    cursor.execute('SELECT * FROM user_ WHERE userid = ?', user_id)
    user= cursor.fetchone()
    user_dict = {
        'userid': user[0],
        'username': user[1],
        'email': user[2],
        'password': user[3],
        # Add more fields as needed
    }
    cursor.close()
    conn.close()
    if user is None:
        abort(404)
    return jsonify(user_dict)
# Update a user
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = request.json
    if not user:
        abort(400)
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    query = "UPDATE user_ SET name = ?, email = ?, password = ? WHERE userid = ?"
    values = (user['name'], user['email'], user['password'], user_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="User updated successfully")
# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_ WHERE userid = ?",user_id)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="User deleted successfully")
# # Post/Blog API

# # Create a new post/blog
@app.route('/posts', methods=['POST'])
def create_post():
    post=request.get_json()
    if not post:
        return jsonify(message="Please provide data"), 400
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    query = "INSERT INTO blog (postid,title, description_, content) VALUES (?, ?,?,?)"
    values = (post['postid'],post['title'], post['description'], post['content'])
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="Post created successfully"), 201
# # Get a specific post/blog
@app.route('/posts/<string:post_id>', methods=['GET'])
def get_post(post_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog WHERE postid = ?', post_id)
    user= cursor.fetchone()
    user_dict = {
        'postid': user[0],
        'title': user[1],
        'description': user[2],
        'content': user[3],
        # Add more fields as needed
    }
    cursor.close()
    conn.close()
    if user is None:
        abort(404)
    return jsonify(user_dict)
# Update a post/blog
@app.route('/posts/<string:post_id>', methods=['PUT'])
def update_post(post_id):
    post = request.get_json()
    if not post:
        abort(400)
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    query = "UPDATE blog SET title = ?, description_ = ?, content = ? WHERE postid = ?"
    values = (post['title'], post['description'], post['content'], post_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="Post updated successfully")
# Delete a post/blog
@app.route('/posts/<string:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blog WHERE postid = ?",post_id)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="Post deleted successfully")

# Create a new like
@app.route('/likes', methods=['POST'])
def create_like():
    like = request.json
    if not like:
        abort(400)
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    query = "INSERT INTO Like_ (postid, userid,likeid) VALUES (?, ?,?)"
    values = (like['post_id'], like['user_id'],like['like_id'])
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="Like created successfully"), 201
# Get a specific like
@app.route('/likes/<string:like_id>', methods=['GET'])
def get_like(like_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Like_ WHERE likeid = ?",like_id)
    like = cursor.fetchone()
    cursor.close()
    conn.close()
    user_dict = {
        'likeid': like[0],
        'userid': like[1],
        'postid': like[2]
        # Add more fields as needed
    }
    if user_dict is None:
        abort(404)
    return jsonify(user_dict)
# Update a like
@app.route('/likes/<string:like_id>', methods=['PUT'])
def update_like(like_id):
    like = request.get_json()
    if not like:
        abort(400)
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    query = "UPDATE Like_ SET postid = ?, userid = ? WHERE likeid = ?"
    values = (like['post_id'], like['user_id'], like_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="Like updated successfully")

# Delete a like
@app.route('/likes/<string:like_id>', methods=['DELETE'])
def delete_like(like_id):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Madhav\SQLEXPRESS;DATABASE=cafe;')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Like_ WHERE likeid = ?",like_id)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify(message="Like deleted successfully")

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/create', methods=['POST'])
# def create_user():
#     user = request.json
#     if not user:
#         return jsonify(message="Please provide data"), 400

#     conn = pyodbc.connect(**db_config)
#     cursor = conn.cursor()
#     query = "INSERT INTO [User] (name, email, password) VALUES (?, ?, ?)"
#     values = (user['name'], user['email'], user['password'])
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify(message="User created successfully"), 201
# Get a specific user
# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "SELECT * FROM User WHERE user_id = %s"
#     values = (user_id,)
#     cursor.execute(query, values)
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if user is None:
#         abort(404)
#     return jsonify(user)

# # Update a user
# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user = request.json
#     if not user:
#         abort(400)
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "UPDATE User SET name = %s, email = %s, password = %s WHERE user_id = %s"
#     values = (user['name'], user['email'], user['password'], user_id)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="User updated successfully")

# # Delete a user
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "DELETE FROM User WHERE user_id = %s"
#     values = (user_id,)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="User deleted successfully")

# # Post/Blog API

# # Create a new post/blog
# @app.route('/posts', methods=['POST'])
# def create_post():
#     post = request.json
#     if not post:
#         abort(400)
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "INSERT INTO Post (title, description, content) VALUES (%s, %s, %s)"
#     values = (post['title'], post['description'], post['content'])
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify(message="Post created successfully"), 201

# # Get a specific post/blog
# @app.route('/posts/<int:post_id>', methods=['GET'])
# def get_post(post_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "SELECT Post.*, COUNT(Like.post_id) as likes_count " \
#             "FROM Post LEFT JOIN `Like` ON Post.post_id = `Like`.post_id " \
#             "WHERE Post.post_id = %s " \
#             "GROUP BY Post.post_id"
#     values = (post_id,)
#     cursor.execute(query, values)
#     post = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if post is None:
#         abort(404)
#     post_data = {
#         'post_id': post[0],
#         'title': post[1],
#         'description': post[2],
#         'content': post[3],
#         'likes_count': post[4]
#     }
#     return jsonify(post_data)

# # Update a post/blog
# @app.route('/posts/<int:post_id>', methods=['PUT'])
# def update_post(post_id):
#     post = request.json
#     if not post:
#         abort(400)
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "UPDATE Post SET title = %s, description = %s, content = %s WHERE post_id = %s"
#     values = (post['title'], post['description'], post['content'], post_id)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="Post updated successfully")

# # Delete a post/blog
# @app.route('/posts/<int:post_id>', methods=['DELETE'])
# def delete_post(post_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "DELETE FROM Post WHERE post_id = %s"
#     values = (post_id,)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="Post deleted successfully")

# # Like API

# # Create a new like
# @app.route('/likes', methods=['POST'])
# def create_like():
#     like = request.json
#     if not like:
#         abort(400)
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "INSERT INTO `Like` (post_id, user_id) VALUES (%s, %s)"
#     values = (like['post_id'], like['user_id'])
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify(message="Like created successfully"), 201

# # Get a specific like
# @app.route('/likes/<int:like_id>', methods=['GET'])
# def get_like(like_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "SELECT * FROM `Like` WHERE like_id = %s"
#     values = (like_id,)
#     cursor.execute(query, values)
#     like = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if like is None:
#         abort(404)
#     return jsonify(like)

# # Update a like
# @app.route('/likes/<int:like_id>', methods=['PUT'])
# def update_like(like_id):
#     like = request.json
#     if not like:
#         abort(400)
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "UPDATE `Like` SET post_id = %s, user_id = %s WHERE like_id = %s"
#     values = (like['post_id'], like['user_id'], like_id)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="Like updated successfully")

# # Delete a like
# @app.route('/likes/<int:like_id>', methods=['DELETE'])
# def delete_like(like_id):
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     query = "DELETE FROM `Like` WHERE like_id = %s"
#     values = (like_id,)
#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     if cursor.rowcount == 0:
#         abort(404)
#     return jsonify(message="Like deleted successfully")

# if __name__ == '__main__':
#     app.run(debug=True)
