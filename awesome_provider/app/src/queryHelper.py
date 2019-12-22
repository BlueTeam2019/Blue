import MySQLdb
class QueryHelper():

    url = ""
    usr = ""
    password = ""
    dbName = ""

    def __init__(self , url, usr, password, dbName):
        self.url = url
        self.usr = usr
        self.password = password
        self.dbName=dbName
        
    def GetConnection():
        return MySQLdb.connect(host=url,    # your host, usually localhost
                        user=usr,         # your username
                        passwd=password,  # your password
                        db=dbName,
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
        db.close()
        return data[0][0]
