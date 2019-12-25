
import json


class Model(object):
    def __init__(self, query_helper):
        self.query = query_helper

    def check_health(self):
        data = self.query.select_one()
        if int(data[0][0]) == 1:
            return True
        return False
    
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
