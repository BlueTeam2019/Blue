import pymysql
import sys
class QueryHelper():            
    #def __init__(self , url, usr, password, dbName, port):
    #    self.url = url
    #    self.usr = usr
    #    self.password = password
    #    self.dbName=dbName
    #    self.port               

    def GetConnection():
        return pymysql.connect(host="mysql",    # your host, usually localhost
                        user="root",                # your username
                        passwd="pass",            # your password
                        db="mysql",                 # name of the data base
                        port=3306)                  # port of the data base

    def AlterData(query):
        returnValue = ""
        if query != "":
            try:
                db = pymysql.connect(host="mysql",    # your host, usually localhost
                            user="root",              # your username
                            passwd="pass",          # your password
                            db="billdb",               # name of the data base
                            port=3306)                # port of the data base
                if db:
                    print("DB ALIVE")
                cur = db.cursor()
                print("after cursor")
                returnValue =  str(cur.execute(query))
                print("after execute")
                db.commit()
                print("after commit")
                print("Rows Changed:{}".format(returnValue))
            except:
                returnValue = "-1"
                print("Error in function: AlterData() please check")
            finally:
                db.close()                    
        return returnValue
    
    def GetData(query):
        returnValue = ""
        if query != "":
             try:
                db = pymysql.connect(host="mysql",    # your host, usually localhost
                            user="root",              # your username
                            passwd="pass",          # your password
                            db="billdb",               # name of the data base
                            port=3306)                # port of the data base
                
                cur = db.cursor()            
                cur.execute(query)                                
                data = cur.fetchall()                                            
                returnValue = data
             except:
                print("Error in function: GetmysqlData() please check")
             finally:
                 if db:
                    db.close()
         
        return returnValue

    def selectOne():
        value = 0
        try:            
            db = pymysql.connect(host="mysql",    # your host, usually localhost
                            user="root",              # your username
                            passwd="pass",          # your password
                            db="mysql",               # name of the data base
                            port=3306)                # port of the data base
            print("After connect")
            cur = db.cursor()            
            cur.execute(""" select 1  """)            
            data = cur.fetchall()                          
            value = data[0][0]
            print(value)
        except:
            print("Error in function: selectOne() please check")
        finally:
            if db:
                db.close()
                    
        return int(value)

