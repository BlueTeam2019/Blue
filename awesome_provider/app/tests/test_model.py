from unittest import TestCase, mock

from model_builder import ModelBuilder


class ModelTest(TestCase):

    #db need to be up with docker-compose-test.yml
    def test_get_one_db_rtn_true(self):
        model = ModelBuilder().build()
        is_alive = model.check_health()
        self.assertEqual(True, is_alive)

    #no db!!!!!!!!!!!!!!!!!!
    def test_get_one_db_rtn_false(self):
        model = ModelBuilder().build()
        is_alive = model.check_health()
        self.assertEqual(False, is_alive)
