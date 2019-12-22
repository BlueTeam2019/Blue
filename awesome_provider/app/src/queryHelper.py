import MySQLdb
class QueryHelper():
    
    def GetConnection():
        return MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                        user="root",         # your username
                        passwd="secret",  # your password
                        db="mysql",
                        port=3306)        # name of the data base

<<<<<<< HEAD:awesome_provider/app/src/QueryHelper.py
    db = None

    def __init__(self , url, usr, password, dbName):
        self.db = MySQLdb.connect(host=url,    # your host, usually localhost
                        user=usr,         # your username
                        passwd=password,  # your password
                        db=dbName)        # name of the data base
        
=======
   # def __init__(self , url, usr, password, dbName):
   #     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
   #                     user="root",         # your username
   #                     passwd="1",  # your password
   #                     db="mysql")        # name of the data base
        expression
>>>>>>> 2f44328ec3089f7360f20157bb49f7827610cdeb:awesome_provider/app/src/queryHelper.py

    
    def selectOne():
        db = GetConnection()
            # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like
<<<<<<< HEAD:awesome_provider/app/src/QueryHelper.py
        cur.execute("SELECT 1;")
        row = cur.fetchall()
=======
        test = cur.execute("SELECT 1;")
        print(test)

>>>>>>> 2f44328ec3089f7360f20157bb49f7827610cdeb:awesome_provider/app/src/queryHelper.py
        # print all the first cell of all the rows
        #for row in cur.fetchall():
        #    print row[0]

        db.close()