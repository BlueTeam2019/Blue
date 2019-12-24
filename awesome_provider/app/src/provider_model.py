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

    def update_truck_provider(truck_id, new_provier_id):
        is_updated = False
        query = "UPDATE Trucks SET provider_id = {} WHERE truck_id = '{}'".format(provider_id,truck_id)
        affected_rows = queryHelper.QueryHelper.AlterData(query)
        if affected_rows == "1":
            is_updated = True
        return is_updated
    def check_if_provider_exist(provider_id):
        provider_exist = False
        query = "SELECT COUNT(*) FROM Provider WHERE id={}".format(provider_id)
        provider_count = queryHelper.QueryHelper.GetData(query)
        if provider_count:
            if provider_count[0][0] == 1:
                provider_exist = True
        return provider_exist

    def insert_truck(provider_id,truck_id):
        is_registered = False
        add_truck_query = "INSERT IGNORE INTO Trucks(id,provider_id) VALUES ('{}',{})".format(truck_id, provider_id)
        print(add_truck_query)
        affected_rows = queryHelper.QueryHelper.AlterData(add_truck_query)
        print(affected_rows)
        if affected_rows == "1":
            is_registered = True
        return  is_registered



    # Register truck:
    # if truck exist wont register
    # for error / no affected rows return False
    def register_truck(request):
        is_registered = False
        if request['id'] and request['provider']:
            truck_id = request['id']
            provider = int(request['provider'])
            if provider_model.check_if_provider_exist(provider):
                is_registered = provider_model.insert_truck(provider,truck_id)
        return is_registered


        
        