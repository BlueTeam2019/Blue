from unittest import TestCase, mock
from src import routing


class RoutingTest(TestCase):

    def setUp(self):
        self.app = routing.app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    @mock.patch("src.provider_routing.model")
    def test_get_health_200(self, mock_model):
        mock_model.check_health.return_val = True
        response = self.client.get('/health')
        self.assertEqual(200, response.status_code)

