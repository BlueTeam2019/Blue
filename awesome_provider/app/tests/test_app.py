from unittest import TestCase
from unittest.mock import MagicMock
from src import provider_routing #, db, mail
from src.provider_model import provider_model
from queryHelper import QueryHelper

class AppTest(TestCase):
    # executed prior to each test
    def setUp(self):
        provider_routing.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        provider_routing.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #     os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = provider_routing.test_client()
        # db.drop_all()
        # db.create_all()
 
        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
    def test_get_health_200(self):
        self.app.CheckHealth = MagicMock(return_value=3)
        response = self.app.get('/')
        self.assertEqual(response, 200)

if __name__ == "__main__":
     unittest.main()

#python3 -m venv virt
#source virt/bin/activate
#sudo apt install default-libmysqlclient-dev
#pip3 install -r requierments.txt
#python -m unittest discover tests/