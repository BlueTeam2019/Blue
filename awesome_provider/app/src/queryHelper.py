import pymysql
class QueryHelper():            
    #def __init__(self , url, usr, password, dbName, port):
    #    self.url = url
    #    self.usr = usr
    #    self.password = password
    #    self.dbName=dbName
    #    self.port       
   
 
    

    def GetConnection():
        return pymysql.connect(host="mysql",    # your host, usually localhost
                        user="api",                # your username
                        passwd="pass",            # your password
                        db="mysql",                 # name of the data base
                        port=3306)                  # port of the data base 
           
     
    def selectOne():
        value = 0
        try:
            print("before connect")
            db = pymysql.connect(host="0.0.0.0",    # your host, usually localhost
                            user="root",              # your username
                            passwd="pass",          # your password
                            db="mysql",               # name of the data base
                            port=33060)                # port of the data base    
            print("after connect")                                        
            cur = db.cursor()
            print("after cursor")                                        
            cur.execute(""" select 1  """)
            data = cur.fetchall()  
            print("after fetchall")                                                     
            value = data[0][0]
            print(value)
        
        except:
            print("Error in function: selectOne() please check")
        finally:
            db.close()
                    
        return int(value)

