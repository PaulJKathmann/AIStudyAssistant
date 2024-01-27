from openai import OpenAI
from chatbot.utils import num_tokens_from_messages
import time
import textstat
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai = OpenAI()

class conversation_manager():

    # prompt : generated using prompt_generator
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.messages = [
            {"role": "system", "content": prompt}
        ]
        self.conversation_cache = [
            {"role": "system", "content": prompt}
        ]

        # messages: remembers the conversation. The messages data structure keeps on modifying to facilitate the limitation of 4096 tokens
        # conversation_cache: This data structure is very similar to the messages ds. However, it is some sort of a database
        # which cannot be modified, but we can only add conversations to it.To facilitate

    # Send input_text to GPT and get the generated response.

    def get_gpt_response(self, input_text, max_response_tokens=500, max_retries=3, base_wait_time=2):

        overall_max_tokens = 4096
        prompt_max_tokens = overall_max_tokens - max_response_tokens

        formatted_query = {"role": "user", "content": input_text}

        self.messages.append(formatted_query)
        # Adding the query to the cache
        self.conversation_cache.append(formatted_query)
        # print(self.messages)
        # To check if the prompt has tokens within the limit
        token_count = num_tokens_from_messages(self.messages)
        # print(f"Token_Count: {token_count}")

        while token_count > prompt_max_tokens:
            print(f"Deleting the message: { self.messages[1]}")
            # We can pop the element 1 to keep the context(system) alive [rather than 0]
            self.messages.pop(1)  # To keep the prompt intact
            token_count = num_tokens_from_messages(self.messages)

        for retry in range(max_retries):
            try:
                print(f"sending to chatgpt: {self.messages}")
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo-1106", temperature=0.8, max_tokens=500, messages=self.messages)                
                # the response from the assistant is saved into the chat history(messages)
                self.messages.append(dict(response.choices[0].message))
                print(
                    f"Response from chatgpt: {response.choices[0].message}")
                # Adding to the response to the cache
                self.conversation_cache.append(
                    response.choices[0].message)
                return response.choices[0].message.content

            except openai.error.APIConnectionError as e:
                wait_time = base_wait_time * \
                    (2 ** retry)  # Exponential backoff
                time.sleep(wait_time)
                continue
        raise Exception("Max retries reached.")

    def print_conversation(self):
        for i in self.conversation_cache:
            print(f"{i['role']}: {i['content']}")

    # used later to save the conversation
    def get_conversationCache(self):
        return self.conversation_cache

    def clear_cm(self):
        # Resetting messages and conversation cache
        self.messages.clear()
        self.conversation_cache.clear()
        self.messages.append({"role": "system", "content": self.prompt})
        self.conversation_cache.append(
            {"role": "system", "content": self.prompt})
                
        print("Bot: \n" + text_bot)
        print("User: \n" + text_user)
        
