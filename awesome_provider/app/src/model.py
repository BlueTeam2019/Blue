<<<<<<< HEAD
import queryHelper
import json
class Model(object):
    #def __init__(self , url, usr, password, dbName):
     #   self.query = QueryHelper(url, usr, password, dbName)
 def __init__(self, query_helper):
        self.query = query_helper

    def check_health(self):
        data = self.query.select_one()
        if int(data[0][0]) == 1:
            return True
        return False



    
    
    def isColumnInProviderExist(self,column,name):
        isExist=0
        isExist=queryHelper.QueryHelper.GetData("select Count(*) from Provider where {}='{}';".format(column,name))
        isExist=isExist[0][0]
        print(isExist)
        if isExist == 0: 
            return 0
        return 1   


    def createProvider(name):
        isNameExist=provider_model.isColumnInProviderExist("name",name)
        result=0
        if isNameExist == 0: 
            print("name is not exist")
            sql=queryHelper.QueryHelper.GetData("INSERT INTO Provider (`name`) VALUES ('{}');".format(name))
            getId=queryHelper.QueryHelper.GetData("select id from Provider where name='{}';".format(name))
            data={'id': getId[0][0] }
            result=json.dumps(data)
        print(result)
        return result


    def updateProvider(self,id ,name):
        isIdExist=-1
        isIdExist=isColumnInProviderExist("id",id)
        #all=queryHelper.QueryHelper.GetData("select * from Provider;")
        #print(all)
        #isIdExist=isIdExist[0][0]
        print(isIdExist)
        if isIdExist != 0: 
            isNameExist=provider_model.isColumnInProviderExist("name",name)
            if isNameExist == 0:
                sql = "UPDATE Provider SET  name='{}' where id ={};".format(name,id)
                return "Update succedded" ,200
            return "The name is exist" ,404
            #isIdExist=queryHelper.QueryHelper.AlterData(sql)
            #print(isIdExist)
            
        return  "The id is not exist" ,404
        
# SELECT COUNT(*)
# FROM information_schema.statistics
# WHERE TABLE_SCHEMA = DATABASE()
#   AND TABLE_NAME = 'Provider' 
#   AND INDEX_NAME = 'name'; 
=======

class Model(object):
    def __init__(self, query_helper):
        self.query = query_helper

    def check_health(self):
        data = self.query.select_one()
        if int(data[0][0]) == 1:
            return True
        return False
>>>>>>> ccadbb36047d4ae5581542c5b701ccd6b0bd8684
