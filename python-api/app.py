'''Test'''

from flask import Flask, jsonify
import psycopg2
from requests import request

app = Flask(__name__)

# Connect to the database
try:
    conn = psycopg2.connect(dbname="your-database-name", user="your-username", 
    password="your-password", host="localhost")
except psycopg2.Error as e:
    print("Error connecting to database: ", e)

# Create a cursor
cur = conn.cursor()

# Define routes
@app.route('/')

def hello():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    # Execute a query to get all users
    try:
        cur.execute("SELECT * FROM users")
    except psycopg2.Error as e:
        print("Error executing SELECT statement: ", e)
        return jsonify({"error": str(e)})

    # Fetch the results
    rows = cur.fetchall()

    # Build a response
    response = []
    for row in rows:
        response.append({
            "id": row[0],
            "name": row[1]
        })

    # Return the response as JSON
    return jsonify(response)


# Close the cursor and connection when the app shuts down
@app.teardown_appcontext
def close_db(error):
    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run()
