import unittest
from unittest import mock

from bill_helper import BillHelper
from model_builder import ModelBuilder


class MyTestCase(unittest.TestCase):
    def test_json(self):
        bill = BillHelper(None, "url")
        session1 = {'product': 'prod name 1'}
        session2 = {'product': 'prod name 2'}
        products = [bill.create_product(13, session1), bill.create_product(145, session2)]
        json = bill.get_json(23, 1230, 1330, 150000, 34, 45, products, "prov name")
        print(json)

    def test_get_data(self):
        id = 23
        f = 0
        t = 1

        bill = BillHelper(ModelBuilder().build(), "url")
        total_pay, truck_count, session_count, \
        products, provider_name = bill.get_data(id, f, t)
        self.assertEqual(total_pay, 60)


if __name__ == '__main__':
    unittest.main()
