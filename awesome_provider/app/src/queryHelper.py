import MySQLdb


class QueryHelper():
   # def __init__(self , url, usr, password, dbName):
   #     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
   #                     user="root",         # your username
   #                     passwd="1",  # your password
   #                     db="mysql")        # name of the data base 
    
    def GetConnection():
        return MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                        user="root",                # your username
                        passwd="secret",            # your password
                        db="mysql",                 # name of the data base
                        port=3306)                  # port of the data base 
           

   
        
    def selectOne():
        value = 0
        try:
            db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                        user="root",              # your username
                        passwd="secret",          # your password
                        db="mysql",               # name of the data base
                        port=3306)                # port of the data base    
            cur = db.cursor()
            cur.execute(""" select 1  """)
            data = cur.fetchall()       
            value = data[0][0]
            print(value)
        
        except:
            print("Error in function: selectOne() please check")
        finally:
            db.close()
                    
        return int(value)

