import queryHelper
query = None

def __init__(self , url, usr, password, dbName):
    self.query = QueryHelper(url, usr, password, dbName)

def CheckHealth():
    #TODO: Call connection to db method / run select 1 from helper        
    try:
        one = query.selectOne()
    except expression as identifier:
        print("DB ERROR")
    return one

