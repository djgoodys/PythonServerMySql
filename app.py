import sys
from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)  # Enable CORS for all routes
CORS(app, origins=["http://localhost:3000"])
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_tnJimgAkaMP36guFO_1'
app.config['MYSQL_DB'] = 'defaultdb'
app.config['MYSQL_HOST'] = 'filtermanager-mysql-filtermanager.e.aivencloud.com'
app.config['MYSQL_PORT'] = 25607

mysql = MySQL(app)

@app.route('/api/manageEquipment', methods=['GET'])
def handleManageEquipment():
    from equipmentView import manageEquipment
    return manageEquipment()

@app.route('/api/manageUsers', methods=['GET'])
def handleManageUsers():
    from usersView import manageUsers
    return manageUsers()

@app.route('/api/manageFilters', methods=['GET'])
def handleManageFilter():
    from filtersView import manageFilters
    return manageFilters()

@app.route('/api/manageFilterTypes', methods=['GET'])
def handleManageFilterTypes():
    from filtertypesView import manageFilterTypes
    return manageFilterTypes()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

