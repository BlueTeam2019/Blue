import os

from model import Model
from query_helper import QueryHelper


class ModelBuilder(object):
    def build(self):
        db_url = os.environ['DB_URL']
        db_user = os.environ['DB_USR']
        db_pass = os.environ['DB_PASS']
        db_name = os.environ['DB_NAME']
        db_port = int(os.environ['DB_PORT'])

        qHelper = QueryHelper(db_url, db_user, db_pass, db_name, db_port)
        return Model(qHelper)