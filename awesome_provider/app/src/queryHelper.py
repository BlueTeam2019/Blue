import MySQLdb


class QueryHelper():
    
    
    def GetConnection():
        return MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                        user="root",         # your username
                        passwd="secret",  # your password
                        db="mysql",
                        port=3306)        # name of the data base
           

   # def __init__(self , url, usr, password, dbName):
   #     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
   #                     user="root",         # your username
   #                     passwd="1",  # your password
   #                     db="mysql")        # name of the data base
        
    def selectOne():
        db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                        user="root",         # your username
                        passwd="secret",  # your password
                        db="mysql",
                        port=3306)        # name of the data base                  
                           
        cur = db.cursor()
        cur.execute(""" select 1  """)
        data = cur.fetchall()       
        print(data)
        print(data[0])
        print(data[0][0])
        db.close()
        return data[0][1]
