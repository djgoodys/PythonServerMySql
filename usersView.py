import json
from flask import request, Response, jsonify
from app import mysql  # Adjust the import to reference mysql

def manageUsers():
    action = request.args.get('action')
    username = request.args.get('username')
    password = request.args.get('password')

    if action == "login":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users;")  # Execute your SQL query
        rv = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

        # Get the query result (you can adjust this based on your needs)
        query_result = [dict(zip(column_names, row)) for row in rv] 

        for row in rv:
            user_data = dict(zip(column_names, row))
            login_passed = False
            if user_data['user_name'] == username and user_data['password'] == password:
                login_passed = True
                user_data['login'] = "passed"
                cur.close()
                # Add the query result to the response headers
                response = jsonify(user_data)
                response.headers['X-Query-Result'] = json.dumps(user_data) 
                return response
            
            if(login_passed == False):
                response = jsonify("{login:'failed'}")
                return response
        cur.close()
        return Response('{"error": "Invalid credentials"}', status=401, mimetype='application/json')

    return Response('{"error": "Invalid action"}', status=400, mimetype='application/json')