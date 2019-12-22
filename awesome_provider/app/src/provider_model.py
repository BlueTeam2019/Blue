import queryHelper


def CheckHealth():
    #TODO: Call connection to db method / run select 1 from helper        
    isAlive = False
    try:        
        if queryHelper.QueryHelper.selectOne() == 1:
            isAlive = True
    except ex:
        print("DB ERROR")
    return isAlive