import requests
import json





class BillHelper(object):

    def __init__(self, model, wight_url):
        self.model = model
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
        trucks = self.get_truck(id)
        provider_name = self.get_provider_name(id)
        products = {}
        total_pay = 0
        truck_count = 0
        session_count = 0

        for t in trucks:
            if t in weights_dict:
                truck_count += 1
                for session in weights_dict[t]:
                    session_count += 1
                    total_pay = \
                        total_pay + self.add_weight(id, products, session)

        return total_pay, truck_count, session_count, products, provider_name

    def map_weight(self, weights_set):
        map = {}
        for w in weights_set:
            if not map[w['id']]: map[w['id']]
            map[w['id']] = w
        return map

    def add_weight(self, id, products, session):
        if session['neto'] == 'na': return 0

        if session['product'] not in products:
            rate = self.get_rate(id, session)
            to_add = self.create_product(rate, session)
            products[session['product'], to_add]
        p = products['product']
        p['count'] = p['count'] + 1
        p['total_kg'] = p['total_kg'] + session['neto']
        add_to_total = p['rate'] * session['neto']
        p['pay'] = p['pay'] + add_to_total
        return add_to_total

    def create_product(self, rate, session):
        to_add = {'name': session['product'], 'count': 0,
                  'rate': rate, 'total_kg': 0, 'pay': 0}
        return to_add

    def get_rate(self, id, session):
        #return self.model \
        #    .get_rate(session['product'], id)

        ##  returns mock ##

        if session['produce'] == "appal": return 1
        if session['produce'] == "banana": return 2

    def get_weights(self, from_t, to_t):
        #issue: pass as parameters ?from_t=<int>&to_t=<int>&f="out"
        #response = requests.get(self.weight_url, from_t, to_t, "out")
        #return json.loads("response")

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

    def get_provider_name(self, id):
        # return self.model.get_provider_by_id(id)
        return "prov name"
    def get_truck(self, id):
        #return self.model.get_trucks(id)
        return {1,2,3,4,5}