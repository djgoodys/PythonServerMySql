from flask import request, jsonify
from app import mysql 
import MySQLdb  


def manageFilterTypes():
    action = request.args.get('action')
    type = request.args.get('filter_type')
    trackable = request.args.get('trackable')

    if action == "get-filter-types":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM filter_types;")
        rv = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        filter_types_list = [dict(zip(column_names, row)) for row in rv]
        cur.close()
        return jsonify(filter_types_list)

    elif action == "create-filter-type":
        try:
            print("starting create the filter-type")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO filter_types(type, trackable) VALUES(%s, %s);", (type, trackable))
            mysql.connection.commit()
            cur.execute("SELECT * FROM filter_types;") 
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filter_types_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filter_types_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error updating filter type: {error}")
            return jsonify({"error": str(error)}), 500
    
    
    elif action == "update-filter-type":
        try:
            if(request.args.get('id')) != None:
                id = int(request.args.get('id'))
            type = request.args.get('filter_type')
            isTrackable = int(trackable)
            cur = mysql.connection.cursor()
            cur.execute("UPDATE filter_types SET type = %s, trackable = %s WHERE _id = %s", (type, isTrackable, id))
            mysql.connection.commit()
            cur.execute("SELECT * FROM filter_types;") 
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filter_types_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filter_types_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error updating filter type: {error}")
            return jsonify({"error": str(error)}), 500
    
    
    if action == "delete-filter-type":
        id = int(request.args.get('id'))
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM filter_types WHERE _id = %s", (id,))
            mysql.connection.commit()

            # Fetch all filters (optional, depending on your needs)
            cur.execute("SELECT * FROM filter_types;")
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filter_types_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filter_types_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error deleting filter type: {error}")
            return jsonify({"error": str(error)}), 500

        finally:
            cur.close()
            
    return "Invalid action", 400