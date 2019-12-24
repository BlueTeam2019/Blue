import queryHelper

class Model:
    def __init__(self, qHelper):
        self.query = qHelper

    def check_health(self):
        isAlive = False
        try:
            if queryHelper.QueryHelper.selectOne() == 1:
                isAlive = True
        except:
            print("DB ERROR")
        return isAlive
