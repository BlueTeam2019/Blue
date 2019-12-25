import pymysql


class QueryHelper(object):
    def __init__(self, url, usr, password, db_name, port):
        self.url = url
        self.usr = usr
        self.password = password
        self.dbName = db_name
        self.port = port

    def get_connection(self):
        return pymysql.connect(host=self.url,  # your host, usually localhost
                               user=self.usr,  # your username
                               passwd=self.password,  # your password
                               db=self.dbName,  # name of the data base
                               port=self.port)  # port of the data base

    def alter_data(self, query):
        return_value = ""
        db = None
        if query:
            try:
                db = self.get_connection()
                cur = db.cursor()
                return_value = f"{cur.execute(query)}"
                db.commit()
                print(f"Rows Changed:{return_value}")

            except pymysql.err as e:
                return_value = "-1"
                print(f"Error in function: GetmysqlData() please check.\n{e}")
            finally:
                if db:
                    db.close()

        return return_value

    def get_data(self, query):
        db = None
        return_value = ""
        if query:
            try:
                db = pymysql.connect(host=self.url,  # your host, usually localhost
                                     user=self.usr,  # your username
                                     passwd=self.password,  # your password
                                     db=self.dbName,  # name of the data base
                                     port=self.port)  # port of the data base

                cur = db.cursor()
                cur.execute(query)
                data = cur.fetchall()
                return_value = data
            except Exception as e:
                print(f"Error in function: GetmysqlData() please check\n{e}")
                raise

            finally:
                if db:
                    db.close()

        return return_value

    def select_one(self):

        return self.get_data(""" select 1  """)
