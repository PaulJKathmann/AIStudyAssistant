from chatbot.user import User
import os

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class prompt_generator():
    def __init__(self, user: User) -> None:
        self.user = user

    def generate_prompt(self, topic: str):
        # generate prompt using the obtained details from the database:
        intro_txt = f"Help the student learn a particular about {topic}. The student is a graduate student studying computer science"
        persona_txt = "You should be friendly and positive as you are a teaching assistant and you want to help the student learn."
        student_description = f"You are talking to a student named {self.user.name}."

        role_txt = f"Help the student study {topic} by explaining the concepts at a high level first and then give them simple examples."
        medium_level_txt = "Once the student understands the basics of the concept you can give them more complex examples and start giving them small tasks to complete."

        #expertise_level = "Student has x level of knowledge"  # lists the full 500 words

        prompt = intro_txt + " " + persona_txt + " " + student_description + " " + role_txt + " " + medium_level_txt

        return prompt


