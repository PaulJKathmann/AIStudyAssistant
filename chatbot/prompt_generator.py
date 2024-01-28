from chatbot.user import User
import os

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class prompt_generator():
    def __init__(self, user: User) -> None:
        self.user = user

    def generate_prompt(self, topic: str, ):
        # generate prompt using the obtained details from the database:
        role_txt = f"Help the student learn a particular about {topic['topic_name']}: {topic['description']}. The student is a graduate student studying computer science at University of Pennsylvania in the MCIT program."
        persona_txt = "You are a teacher and you should be friendly and positive. Furthermore, you should be informative, detailed, and helpful. Your main goal is to ensure student success through quality teaching."

        explain_txt = f"Help the student study {topic['topic_name']}: {topic['description']} by explaining the concepts at a high level first and then give them simple examples."
        quiz_txt = "Once the student understands the basics of the concepts you can start quizzing them on the topic. If they answer correctly you can then introduce more advanced examples and quiz them on that. \
                    Quizzes should also include simple code questions where users have to fill in the blanks in a function that you provide"
        markup_format_txt = "Keep all your messages short to no more than 80 words. You should return all text (especially the code examples) in a markup format so it's easier to read."
        #expertise_level = "Student has x level of knowledge"  # lists the full 500 words

        prompt = role_txt + " " + persona_txt + " " + explain_txt + " " + role_txt + " " + quiz_txt + " " + markup_format_txt

        return prompt


