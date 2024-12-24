import sys
from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['MYSQL_USER'] = 'sql3753434'
app.config['MYSQL_PASSWORD'] = 'jW8Lj1AvuT'
app.config['MYSQL_DB'] = 'sql3753434'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/manageEquipment', methods=['GET'])
def handleManageEquipment():
    from equipmentView import manageEquipment
    return manageEquipment()

@app.route('/manageUsers', methods=['GET'])
def handleManageUsers():
    from usersView import manageUsers
    return manageUsers()

@app.route('/manageFilters', methods=['GET'])
def handleManageFilter():
    from filtersView import manageFilters
    return manageFilters()

@app.route('/manageFilterTypes', methods=['GET'])
def handleManageFilterTypes():
    from filtertypesView import manageFilterTypes
    return manageFilterTypes()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

