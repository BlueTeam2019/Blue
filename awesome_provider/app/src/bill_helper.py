import os

import requests
import json


class BillHelper(object):

    def __init__(self, wight_url, model):
        self.data_model = model
        self.weight_url = wight_url

    def get_json(self, id, from_t, to_t, total_pay, \
                 truck_count, session_count, products, provider_name):
        response = {'id': id, 'name': provider_name, 'from': from_t,
                    'to': to_t, 'truckCount': truck_count,
                    'sessionCount': session_count, 'products': products, \
                    'total_pay': total_pay}
        return json.dumps(response)

    def get_data(self, id, from_t, to_t):
        weights_set = self.get_weights(from_t, to_t)
        weights_dict = self.map_weight(weights_set)
        trucks_table = self.get_truck(id)
        provider_name = self.get_provider_name(id)
        rates = self.get_rates(id)
        products = {}
        total_pay = 0
        truck_count = 0
        session_count = 0

        for row in trucks_table:
            if row[0] == "I": break
            if int(row[0]) in weights_dict:
                truck_count += 1
                for session in weights_dict[int(row[0])]:
                    session_count += 1
                    total_pay = \
                        total_pay + self.add_weight(id, products,
                                                    session, rates)

        return total_pay, truck_count, \
               session_count, products, provider_name

    def map_weight(self, weights_set):
        map = {}
        for w in weights_set:
            id = w['id']
            if not id in map.keys(): map[id] = []
            map[id].append(w)
        return map

    def add_weight(self, id, products, session, rates):
        if session['neto'] == 'na': return 0
        if session['produce'] not in products:
            rate = rates[session['produce']]
            to_add = self.create_product(rate, session)
            products[session['produce']] = to_add
        p = products[session['produce']]
        p['count'] = p['count'] + 1
        p['total_kg'] = p['total_kg'] + session['neto']
        add_to_total = p['rate'] * session['neto']
        p['pay'] = p['pay'] + add_to_total
        return add_to_total

    def create_product(self, rate, session):
        to_add = {'name': session['produce'], 'count': 0,
                  'rate': rate, 'total_kg': 0, 'pay': 0}
        return to_add

    def get_rates(self, id):
        table = self.data_model.get_rates(id)
        rates = {}
        for row in table:
            if row[2] == "ALL" and \
                    row[0] not in rates or \
                    int(row[2]) == id:
                rates[row[0]] = row[1]
        return rates

    def get_provider_name(self, id):
        return self.data_model.get_provider_by_id(id)

    def get_truck(self, id):
        return self.data_model.get_trucks(id)

    def get_weights(self, from_t, to_t):
        if os.environ["MOCK_WEIGHT"] == "FALSE":
            return self.model_.get_weights(from_t, to_t)
        ##  returns mock ##
        return [{"id": 1,
                 "direction": "out",
                 "bruto": 0,
                 "neto": "na",
                 "produce": "appal",
                 "containers": []},
                {"id": 2,
                 "direction": "out",
                 "bruto": 0,
                 "neto": 10,
                 "produce": "appal",
                 "containers": []},
                {"id": 1,
                 "direction": "out",
                 "bruto": 0,
                 "neto": 10,
                 "produce": "appal",
                 "containers": []},
                {"id": 3,
                 "direction": "out",
                 "bruto": 0,
                 "neto": 20,
                 "produce": "appal",
                 "containers": []},
                {"id": 4,
                 "direction": "out",
                 "bruto": 0,
                 "neto": 10,
                 "produce": "banana",
                 "containers": []},
                {"id": 5,
                 "direction": "in",
                 "bruto": 0,
                 "neto": 10,
                 "produce": "banana",
                 "containers": []},
                {"id": 6,
                 "direction": "in",
                 "bruto": 0,
                 "neto": 10,
                 "produce": "banana",
                 "containers": []}
                ]
