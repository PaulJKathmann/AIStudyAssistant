from chatbot.conversation_manager import conversation_manager
from chatbot.prompt_generator import prompt_generator
from chatbot.user import User
from chatbot.experiment_manager import experiment_manager
import pymongo
import openai
import os
from pymongo import MongoClient
import numpy as np



openai.api_key = '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'
os.environ['OPENAI_API_KEY'] = openai.api_key

client = MongoClient(
    "mongodb+srv://mikth:KWJHqejostbRNm8Z@cluster0.xn2i2bv.mongodb.net/")



class Chatbot():

    def __init__(self, email: str) -> None:
        self.user = User(client=client, email=email)
        self.prompt = prompt_generator(user=self.user).generate_prompt()
        self.cm = conversation_manager(prompt=self.prompt)
        self.em = experiment_manager(user=self.user)
        print("Initialize the chatbot..")

    def get_response(self, text):
        end = 0
        if any(i in text.lower() for i in ["thank", "thanks"]):
            res = np.random.choice(
                ["You're welcome!", "Anytime!", "No problem!", "Cool!"])

        elif any(i in text.lower() for i in ["exit", "close", "shut down", "goodbye", "bye"]):
            res = np.random.choice(["Have a good day!", "Bye.", "Goodbye!"])
            scores = self.cm.get_current_reading_scores()
            
            print("")
            print("The predicted grade for the chatbot is: ",scores["bot_grade"] )
            print("The predicted grade for the user is: ",scores["user_grade"] )
            print("The McApline score for the bot is: ", scores["bot_mcalpine"])
            print("The McAlpine score for the user is: ", scores["user_mcalpine"])
            print("Note:")
            print("1. Grade is calculated by the textstat library based on Flesch Reading Formula, Flesch-Kincaid Grade level, Fog Scale, SMOG Index, Automated Reading Index, Coleman-Liau Index, Linsear Formula and Dale-Chall Readability score.")
            print("2. McAlpine score returns a score for the readability of an english text for a foreign learner or English, focusing on the number of miniwords and length of sentences. Here is the scale: 1-20 (very easy to understand); 21-25 (quite easy to understand); 26-29 (a little difficult); and 30+ (very confusing).")
            
            self.em.save_conversation(self.cm.get_conversationCache(), client = client, scores= scores)
            # Empty messages and conversation_cache
            print("")
            self.cm.clear_cm()
            # print(self.cm.messages)
            end = 1
        else:
            res = self.cm.get_gpt_response(input_text=text)

        return res, end


# import pickle
# client = MongoClient("mongodb+srv://kapadiaaryan09:FuYneFdGHF1A989e@cluster0.rxbbi1v.mongodb.net/?retryWrites=true&w=majority")
# test = Chatbot(client = client, userId="aryan01")
# serialized_chatbot = pickle.dumps(test)
# # response = test.get_response(text = "Hello, how are you?")
# # print(response)
