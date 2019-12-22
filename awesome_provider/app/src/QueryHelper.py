import MySQLdb
class QueryHelper():

    db = None

    def __init__(self , url, usr, password, dbName):
        self.db = MySQLdb.connect(host=url,    # your host, usually localhost
                        user=usr,         # your username
                        passwd=password,  # your password
                        db=dbName)        # name of the data base
        

    
    def selectOne():
            # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like
        cur.execute("SELECT 1;")
        row = cur.fetchall()
        # print all the first cell of all the rows
        #for row in cur.fetchall():
        #    print row[0]

        db.close()