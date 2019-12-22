import queryHelper
def CheckHealth():
    #TODO: Call connection to db method / run select 1 from helper        
    try:
        one = selectOne()
    except expression as identifier:
        print("DB ERROR")
    return one