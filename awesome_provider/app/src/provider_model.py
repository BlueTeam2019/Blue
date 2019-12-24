import queryHelper
import json
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
    
    
    def createProvider(name):
        isNameExist=0
        #TO-DO:check if there is another way
        isNameExist="select Count(*) from Provider where name='{}';".format(name)
        if isNameExist == 0: 
            sql="INSERT INTO Provider (`name`) VALUES ('{}');".format(name)
            getId="select id from Provider where name='{}';".format(name)
            data={'id': getId }
            data=json.dumps(data)
        result=json.dumps(data)
        print(result)
        return result


    def updateProvider(id ,name):
        isNameExist="select Count(*) from Provider where id='{}';".format(id)
        if isNameExist != 0: 
            sql = "UPDATE Provider SET  name='{}' where id ='{}';".format(name,id)
            return 1
        return 0
        
# SELECT COUNT(*)
# FROM information_schema.statistics
# WHERE TABLE_SCHEMA = DATABASE()
#   AND TABLE_NAME = 'Provider' 
#   AND INDEX_NAME = 'name'; 