from flask_mysqldb import MySQL
class QueryHelper(app):

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

def selectOne():
    cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
    cur.execute("SELECT 1;")
    mysql.connection.commit()
    cur.close()

    def __repr__(self):
