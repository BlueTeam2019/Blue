from model_handlers import generate_query_from_excel
import json


class Model(object):
    def __init__(self, query_helper):
        self.query = query_helper

    def check_health(self):
        data = self.query.select_one()
        if int(data[0][0]) == 1:
            return True
        return False

    def update_truck_provider(self, request, new_provider):
        is_updated = False
        if request.get('id') and request.get('provider') and new_provider:
            truck_id = request['id']
            old_provider = int(request['provider'])
            new_provider = int(new_provider)
            if self.check_if_provider_exist(old_provider) and self.check_if_provider_exist(new_provider):
                is_updated = self.update_provider_for_truck(truck_id,new_provider)

        return is_updated

    def check_if_provider_exist(self, provider_id):
        provider_exist = False
        check_provider_query = f"SELECT COUNT(*) FROM Provider WHERE id={provider_id}"
        provider_count = self.query.get_data(check_provider_query)
        if provider_count:
            if provider_count[0][0] == 1:
                provider_exist = True

        return provider_exist

    def update_provider_for_truck(self, truck_id, new_provider_id):
        is_updated = False
        update_truck_query = f"UPDATE Trucks SET provider_id = {new_provider_id} WHERE id = '{truck_id}'"
        affected_rows = self.query.alter_data(update_truck_query)
        if affected_rows == "1":
            is_updated = True
        return is_updated

    def insert_truck(self, provider_id, truck_id):
        is_registered = False
        add_truck_query = f"INSERT IGNORE INTO Trucks(id,provider_id) VALUES ('{truck_id}',{provider_id})"
        affected_rows = self.query.alter_data(add_truck_query)
        if affected_rows == "1":
            is_registered = True

        return  is_registered

    def register_truck(self, request):
        # Register truck:
        # if truck exist wont register
        # for error / no affected rows return False
        is_registered = False
        if request.get('id') and request.get('provider'):
            truck_id = request['id']
            provider = int(request['provider'])
            if self.check_if_provider_exist(provider):
                is_registered = self.insert_truck(provider, truck_id)

        return is_registered

    def is_column_in_provider_exist(self, column, name):
        is_exist = self.query.get_data(f"select Count(*) from Provider where {column}='{name}';")
        is_exist = is_exist[0][0]
        print(is_exist)
        if not is_exist:
            return False
        return True

    def create_provider(self, name):
        """
        Receives a Provider name, checks existence of name then inserts into DB
        :param name: Provider name
        :return:
        """
        is_name_exist = self.is_column_in_provider_exist("name", name)
        result = ''
        if not is_name_exist:
            print("name is not exist")
            self.query.get_data(f"INSERT INTO Provider (`name`) VALUES ('{name}');")
            get_id = self.query.get_data(f"select id from Provider where name='{name}';")
            result = json.dumps({'id': get_id[0][0]})
        print(result)
        return result

    def update_provider(self, id, name):
        is_id_exist = self.is_column_in_provider_exist("id", id)
        print(is_id_exist)
        if is_id_exist:
            is_name_exist = self.is_column_in_provider_exist("name", name)
            if not is_name_exist:
                sql_query = f"UPDATE Provider SET  name='{name}' where id ={id};"
                self.query.alter_data(sql_query)
                return True, "Update succeeded"
            return False, "The name is exist"

        return False, "The id is not exist"

    def post_rates_to_db(self, file):
        table_name = "Rates"

        file_query = generate_query_from_excel(file)

        # First remove all records from the table
        self.query.alter_data(f'''DELETE FROM {table_name};''')
        # Insert new values into the table
        db_records = self.query.alter_data(f'''INSERT INTO {table_name}(product_id, rate, scope) VALUES {file_query};''')

        return int(db_records)

