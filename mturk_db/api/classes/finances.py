from api.classes import Manager_Projects


class Manager_Finances(object):
    @staticmethod
    def get_balance(database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(use_sandbox)
        return {
            'balance': float(client.get_account_balance()['AvailableBalance'])
        }