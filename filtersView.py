from flask import request, jsonify
from app import mysql 
import datetime
from datetime import date, datetime, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

import calendar
from dateutil.relativedelta import relativedelta
import MySQLdb  

def manageFilters():
    action = request.args.get('action')
    filter_size = request.args.get('filter_size')
    notes = request.args.get('notes') 
    count = request.args.get('count') 
    par = request.args.get('par')
    pn = request.args.get('pn')  
    storage = request.args.get('storage') 
    filter_type = request.args.get('filter_type')
    if action == "get-all-filters":
        username = request.args.get('username') 
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM filters;")
        rv = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        filters_list = [dict(zip(column_names, row)) for row in rv]
        cur.close()
        return jsonify(filters_list)
    
    if action == "add-new-filter":
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO filters(filter_size, filter_type, filter_count, par, notes, storage, pn) VALUES(%s, %s, %s, %s, %s, %s, %s);", (filter_size, filter_type, count, par, notes, storage, pn))
            mysql.connection.commit()

            # Fetch all equipment (optional, depending on your needs)
            cur.execute("SELECT * FROM filters;") 
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filters_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filters_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error updating filter: {error}")
            return jsonify({"error": str(error)}), 500
   
    if action == "delete-filter":
        id = int(request.args.get('id'))
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM filters WHERE _id = %s", (id,))
            mysql.connection.commit()

            # Fetch all filters (optional, depending on your needs)
            cur.execute("SELECT * FROM filters;")
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filters_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filters_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error deleting filter: {error}")
            return jsonify({"error": str(error)}), 500

        finally:
            cur.close()

    if action == "update-filter":
        id = int(request.args.get('id'))
        try:
            filter_size = request.args.get('filter_size')
            cur = mysql.connection.cursor()
            cur.execute("UPDATE filters SET filter_size = %s, filter_type = %s, filter_count = %s, par = %s, pn = %s, storage = %s, notes = %s WHERE _id = %s", (filter_size, filter_type, count, par, pn, storage, notes, id,))
            mysql.connection.commit()

            # Fetch all filters (optional, depending on your needs)
            cur.execute("SELECT * FROM filters;")
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            filters_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(filters_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error deleting filter: {error}")
            return jsonify({"error": str(error)}), 500

        finally:
            cur.close()