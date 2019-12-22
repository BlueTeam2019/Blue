import QueryHelper
class provider_model():
    query = None
    def __init__(self , url, usr, password, dbName):
        self.query = QueryHelper(url, usr, password, dbName)

    def CheckHealth():        
        return query.selectOne()