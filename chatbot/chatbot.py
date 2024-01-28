from chatbot.conversation_manager import conversation_manager
from chatbot.prompt_generator import prompt_generator
from chatbot.user import User
import pymongo
import openai
import os
from pymongo import MongoClient
import numpy as np

# This loads the variables from .env

# from dotenv import load_dotenv
# load_dotenv() 


openai.api_key = ''

client = MongoClient("mongodb+srv://kathmann:PRYXSXABxqM0johQ@cluster0.yqfrbpf.mongodb.net/?tls=true&tlsVersion=TLS1.2")


class Chatbot():

    def __init__(self, name: str, topic: str) -> None:
        self.user = User(client=client, name=name)
        self.prompt = prompt_generator(user=self.user).generate_prompt(topic=topic)
        self.cm = conversation_manager(prompt=self.prompt)
        print("Initialize the chatbot..")

    def get_response(self, text):
        end = 0
        if any(i in text.lower() for i in ["thank", "thanks"]):
            res = np.random.choice(
                ["You're welcome!", "Anytime!", "No problem!", "Cool!"])
        else:
            res = self.cm.get_gpt_response(input_text=text)

        return res, end


# import pickle
# client = MongoClient("mongodb+srv://kapadiaaryan09:FuYneFdGHF1A989e@cluster0.rxbbi1v.mongodb.net/?retryWrites=true&w=majority")
# test = Chatbot(client = client, userId="aryan01")
# serialized_chatbot = pickle.dumps(test)
# # response = test.get_response(text = "Hello, how are you?")
# # print(response)
