import queryHelper
import sys

class provider_model:
    #def __init__(self , url, usr, password, dbName):
     #   self.query = QueryHelper(url, usr, password, dbName)

    def CheckHealth():
        print("in CheckHealth()")
        isAlive = False
        try:        
            if queryHelper.QueryHelper.selectOne() == 1:
                isAlive = True
        except:
            print("DB ERROR")
        return isAlive

    # Register truck:
    # if truck exist wont register
    # for error / no affected rows return False
    def register_truck(request):
        print("register_truck")
        is_registered = False
        if request and request['id'] and request['provider']:
            print("if request and request['id'] and request['provider']:")
            truck_id = request['id']
            provider = request['provider']
            check_provider_query = "SELECT COUNT(*) FROM Provider WHERE id={}".format(provider)
            provider_count = queryHelper.GetData(check_provider_query)
            print("provider_count = queryHelper.GetData(check_provider_query)")
            if provider_count:
                print("if provider_count:")
                if provider_count[0][0] == 1:
                    print("if provider_count[0][0] == 1:")
                    add_truck_query = "INSERT IGNORE INTO Trucks (id,provider) VALUES ('{}',{})".format(truckId,provider)
                    affected_rows = queryHelper.AlterData(query)
                    if affected_rows == 1:
                        is_registered = True
        return is_registered


        
        