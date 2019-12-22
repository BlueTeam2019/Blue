from flask_mysqldb import MySQL
class QueryHelper(app):

    mysql

def __init__(self, app, url, usr, password, dbName):
    app.config['MYSQL_HOST'] = url
    app.config['MYSQL_USER'] = usr
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = dbName
    mysql = MySQL(app)

def selectOne():
    cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
    cur.execute("SELECT 1;")
    mysql.connection.commit()
    cur.close()

    
