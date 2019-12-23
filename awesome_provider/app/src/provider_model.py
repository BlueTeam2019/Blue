import queryHelper

class provider_model:
    #def __init__(self , url, usr, password, dbName):
     #   self.query = QueryHelper(url, usr, password, dbName)

    def CheckHealth():
        print("in CheckHealth()")
        #TODO: Call connection to db method / run select 1 from helper        
        isAlive = False
        try:        
            if queryHelper.QueryHelper.selectOne() == 1:
                isAlive = True
        except:
            print("DB ERROR")
        return isAlive