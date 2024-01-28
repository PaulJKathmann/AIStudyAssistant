import pymongo

class User():
    def __init__(self, client: pymongo.mongo_client.MongoClient, name) -> None:
        user_db = client.get_database(
            'AiAssistant').User_Collection
        user = user_db.find_one({'name': name})
        if user:
            self.name = user["name"]
        else:
            print("User not found. Proceeding with user Paul")
            self.name = name

    

        