import unittest
from unittest import TestCase, mock
from src import provider_routing

class AppTest(TestCase):
    # executed prior to each test
    def setUp(self):
        self.app = provider_routing.app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    @mock.patch("src.provider_routing.model")
    def test_get_health_200(self, mock_model):
        mock_model.check_health.return_val = True

        #provider_routing.set_model(mock_model)
        response = self.client.get('/health')
        self.assertEqual(200, response.status_code)


#python3 -m venv virt
#source virt/bin/activate
#sudo apt install default-libmysqlclient-dev
#pip3 install -r requierments.txt
#python -m unittest discover ../tests/