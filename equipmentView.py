from flask import request, jsonify
from app import mysql 
import datetime
from datetime import date, datetime, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

import calendar
from dateutil.relativedelta import relativedelta
import MySQLdb  

def get_today_date():
    today = datetime.today()
    year = today.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    return f"{year}-{month}-{day}"



def get_filter_due_date(rotation):
    from datetime import date
    from datetime import datetime, timedelta
    import calendar
    from dateutil.relativedelta import relativedelta
    next_due_date = datetime.now() + relativedelta(months=rotation)
    formatted_date = next_due_date.strftime("%Y-%m-%d")  
    return formatted_date


def handle_newtasks(newtasks):

    if isinstance(newtasks, str):
        return newtasks.split(',')
    elif isinstance(newtasks, list):
        return newtasks
    else:
        return []  # Handle unexpected input types
    
def manageEquipment():
    action = request.args.get('action')
    username = request.args.get('username')
    if action == "get-all-equipment":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM equipment;")
        rv = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        equipment_list = [dict(zip(column_names, row)) for row in rv]
        cur.close()
        return jsonify(equipment_list)
    
    if action == "get_all_tasks":
            username = request.args.get('username') 
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM equipment WHERE assigned_to = %s", (username,))
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            equipment_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(equipment_list)
        
    if action == "cancel-task":
        unitId = request.args.get('unit_id')
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE equipment SET assigned_to = '' WHERE _id = %s", (unitId,))
            mysql.connection.commit() 

            cur.execute("SELECT * FROM equipment WHERE assigned_to = %s", (username,))
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            equipment_list = [dict(zip(column_names, row)) for row in rv]
            return jsonify(equipment_list) 

        except mysql.connector.Error as error:
            print(f"Failed to update equipment: {error}")
            return jsonify({"error": str(error)}), 500
        finally:
            cur.close()
            
    if action == "add-all-tasks":
        username = request.args.get('username')
        newtasks = request.args.get('newtasks') 
        newtasks_list = handle_newtasks(newtasks)

        cur = mysql.connection.cursor()
        try:
            for task_id in newtasks_list:
                cur.execute("UPDATE equipment SET assigned_to = %s WHERE _id = %s", (username, task_id))
            mysql.connection.commit()

            cur.execute("SELECT * FROM equipment WHERE assigned_to = %s", (username,))
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            equipment_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(equipment_list)

        except mysql.connector.Error as error:
            print(f"Failed to update equipment: {error}")
            return jsonify({"error": str(error)}), 500
        
        finally:
            cur.close()

    if action == "complete-task":
        rotation = request.args.get('rotation')
        username = request.args.get('username')
        unit_id = request.args.get('unit_id') 
        filter_type = request.args.get('filter_type')
        try:
            # Calculate next due date
            next_due_date = get_filter_due_date(int(rotation)) 

            # Update equipment in the database
            cur = mysql.connection.cursor()
            cur.execute("UPDATE equipment SET assigned_to = '', filters_last_changed = %s, filters_due = %s, filter_type = %s WHERE _id = %s", 
                        (f"[{username}]" + get_today_date(), next_due_date, filter_type, unit_id))
            mysql.connection.commit()

            # Fetch all equipment (optional, depending on your needs)
            cur.execute("SELECT * FROM equipment WHERE assigned_to = %s", (username)) 
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            equipment_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(equipment_list)

        except MySQLdb.Error as error:  # Correctly catching MySQLdb errors
            print(f"Error updating equipment: {error}")
            return jsonify({"error": str(error)}), 500
    
    
    if action == "filtersdone":
        rotation = request.args.get('rotation') or 0
        username = request.args.get('username')
        unit_id = request.args.get('unit_id')
        filter_type = request.args.get('filter_type')  

        try:
            # Calculate next due date
            next_due_date = get_filter_due_date(int(rotation)) 

            # Update equipment in the database
            cur = mysql.connection.cursor()
            cur.execute("UPDATE equipment SET assigned_to = '', filters_last_changed = %s, filters_due = %s, filter_type = %s WHERE _id = %s", (f"[{username}]" + get_today_date(), next_due_date, filter_type, unit_id))
            mysql.connection.commit()

            # Fetch all equipment (optional, depending on your needs)
            cur.execute("SELECT * FROM equipment;") 
            rv = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            equipment_list = [dict(zip(column_names, row)) for row in rv]
            cur.close()
            return jsonify(equipment_list)

        except MySQLdb.Error as error:  
            print(f"Error updating equipment: {error}")
            return jsonify({"error": str(error)}), 500
    
    if action == "search":

        searchwords = request.args.get('searchwords')
        searchwords = "%" + searchwords + "%"
        query = """
        SELECT * FROM equipment
        WHERE unit_name LIKE %s
        OR location LIKE %s
        OR area_served LIKE %s
        OR filter_size LIKE %s
        OR filter_type LIKE %s
        OR assigned_to LIKE %s
        OR belts LIKE %s
        OR notes LIKE %s
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (
            searchwords, searchwords, searchwords, 
            searchwords, searchwords, searchwords, searchwords, searchwords
        ))
        rv = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        equipment_list = [dict(zip(column_names, row)) for row in rv]
        cur.close()
        return jsonify(equipment_list)

    if action == "sort":
            sortby = request.args.get('sortby') 
            cur = mysql.connection.cursor()
            if(sortby == "ASC"):
                cur.execute("SELECT * FROM equipment ORDER BY filters_due ASC;")
                rv = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                equipment_list = [dict(zip(column_names, row)) for row in rv]
                cur.close()
                return jsonify(equipment_list)
            
            if(sortby == "DESC"):
                cur.execute("SELECT * FROM equipment ORDER BY filters_due DESC;")
                rv = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                equipment_list = [dict(zip(column_names, row)) for row in rv]
                cur.close()
                return jsonify(equipment_list)
            
            if(sortby == "today"):
                cur.execute("SELECT * FROM equipment WHERE filters_due = CURDATE();")
                rv = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                equipment_list = [dict(zip(column_names, row)) for row in rv]
                cur.close()
                return jsonify(equipment_list)
            
            if(sortby == "NORMAL"):
                cur.execute("SELECT * FROM equipment;")
                rv = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                equipment_list = [dict(zip(column_names, row)) for row in rv]
                cur.close()
                return jsonify(equipment_list)


