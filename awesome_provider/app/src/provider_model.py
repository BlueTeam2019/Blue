from query_helper import QueryHelper


class ProviderModel(object):
    def check_health(self):
        if QueryHelper().select_one() == 1:
            return True
        return False
