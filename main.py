import os
from flask import Flask, request, jsonify
import pymysql  # Use pymysql instead of flaskext.mysql

# Load database credentials from environment variables (recommended)
DB_USER = os.getenv('MYSQL_DATABASE_USER')
DB_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE_DB')
DB_HOST = os.getenv('MYSQL_DATABASE_HOST')

#DB_HOST = 'mert-mysql'

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
# db = SQLAlchemy(app)

# Connect to MySQL database
connection = pymysql.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Person")
            data = cursor.fetchall()
        return jsonify({'tasks': data})
    except Exception as e:
        print(f"Error retrieving tasks: {str(e)}")  # Log the error
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required for a task'}), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Person (content, completed) VALUES (%s, %s)", (content, False))
            connection.commit()
        return jsonify({'message': 'Task added successfully'})
    except Exception as e:
        print(f"Error adding task: {str(e)}")  # Log the error
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081)
