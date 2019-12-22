import MySQLdb

class QueryHelper():

    db

    def __init__(self , url, usr, password, dbName):
        db = MySQLdb.connect(host=url,    # your host, usually localhost
                        user=usr,         # your username
                        passwd=password,  # your password
                        db=dbName)        # name of the data base
        

    def selectOne():
            # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like
        cur.execute("SELECT 1;")

        # print all the first cell of all the rows
        #for row in cur.fetchall():
        #    print row[0]

        db.close()