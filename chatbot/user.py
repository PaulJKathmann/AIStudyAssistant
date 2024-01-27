import pymongo

class User():

    '''
    This function collects, stores, and retrieves user descriptions from our database.
    It first prompts the user to enter an id, if it exists
    If not, then a series of fields are filled in by the user to create a new account,
    which is then stored in the mongodb database.
    '''

    def __init__(self, client: pymongo.mongo_client.MongoClient, name) -> None:
        user_db = client.get_database(
            'AiAssistant').User_Collection
        user = user_db.find_one({'name': name})
        self.name = user["name"]
        # self.name = user["name"]

    

        