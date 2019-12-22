import MySQLdb
class QueryHelper():

    def __init__(self , url, usr, password, dbName, port):
        self.url = url
        self.usr = usr
        self.password = password
        self.dbName=dbName
        self.port

    def GetConnection(self):
        return MySQLdb.connect(host=self.url,    # your host, usually localhost
                        user=self.usr,         # your username
                        passwd=self.password,  # your password
                        db=self.dbName,
                        port=self.port)        # name of the data base
           

    def selectOne():
        db = GetConnection()         
        cur = db.cursor()
        cur.execute(""" select 1  """)
        data = cur.fetchall()               
        db.close()
        return data[0][0]
