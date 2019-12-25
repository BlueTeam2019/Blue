import json
import requests


class Model(object):
    def __init__(self, query_helper):
        self.query = query_helper

    def check_health(self):
        data = self.query.select_one()
        if int(data[0][0]) == 1:
            return True
        return False

    #return trucks {} hash_set by provider id
    def get_trucks(self, id):
        return {}
    def get_provider_by_id(id):
        return 0
    #return int product rate by provider id
    def get_rate(self, products, id):
        return 0

