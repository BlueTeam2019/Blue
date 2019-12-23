import pymysql

DB_CONFIG = {
    "host": "localhost",    # your host, usually localhost
    "user": "root",          # your username
    "passwd": "pass",       # your password
    "db": "billdb",         # name of the data base
    "port": 3306,           # port of the data base
}  # DB_CONFIG


class QueryHelper(object):
    def __init__(self):
        self.db_driver = pymysql.connect(**DB_CONFIG)

    def alter_data(self, query):
        return_value = ""
        if query:
            try:
                cur = self.db_driver.cursor()
                return_value = f"{cur.execute(query)}"
                self.db_driver.commit()
                print(f"Rows Changed:{return_value}")
            except pymysql.err as e:
                return_value = "-1"
                print(f"Error in function: GetmysqlData() please check\n{e}")
            finally:
                self.db_driver.close()

        return return_value
    
    def get_data(self, query):
        return_value = ""
        if query:
            try:
                cur = self.db_driver.cursor()
                cur.execute(query)                                
                data = cur.fetchall()                                            
                return_value = data
            except pymysql.err as e:
                print(f"Error in function: GetmysqlData() please check.\n{e}")
                print(pymysql.err)
                
            finally:
                self.db_driver.close()
         
        return return_value

    def select_one(self):
        value = 0
        try:
            data = self.get_data(""" select 1  """)
            value = int(data[0][0])
        except Exception as e:
            print(f"Error in function: selectOne() please check.\n{e}")

        return value
