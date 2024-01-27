from chatbot.user import User
import os

# language proficiency should be measured as grade-level
# should give defaults so that it will run if no user is given
# future: maybe better to not pass in the user, but the needed attributes??
# would be better to store the prompt as a local variable

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class prompt_generator():

    def __init__(self, user: User) -> None:
        self.user = user

    def read_prompt(self, prompt_name, prompt_type=None):
        folder = "prompts/goals/" if prompt_type == "goal" else "prompts/"
        filepath = os.path.join(BASE_DIR, folder, prompt_name + ".txt")
        with open(filepath, "r") as filename:
            prompt = filename.read()
        return prompt

    def generate_prompt(self, goal='have_fun', role='student', pdftext = None, vocabulary_size=500):
        # generate prompt using the obtained details from the database:
        intro_txt = self.read_prompt("intro")
        persona_txt = "You should be friendly and positive."

        #background = "This is the first time that you are talking to them."
        background = ""
        student_description = f"You are talking to a student named {self.user.name} who is {self.user.age} years old \
        and studies in grade {self.user.grade}. They have studied English for {self.user.lang_proficiency} years."

        if role == 'student':
            role_txt = "You are about the same age as the student and share similar interests."
        if role == 'teacher':
            role_txt = "You are a teacher and can answer questions in their native language."

        #vocab_txt = self.read_prompt("vocabulary")   # lists the full 500 words
        vocab_txt = f"Try to restrict your answers to words the student has used, words related to any topic the student requests, and the {vocabulary_size} most common English words."

        
        do_not = self.read_prompt("do_not")

        if goal == 'learn_words':
            session_goal = "The goal of this session is for the student to practice the following words: \
                        cat, mouse, hat, coat, mittens. Start my telling the student that, listing the words. Then \
                        please try to use these words in your conversation."
        elif goal == 'discuss_text':
            if pdftext is None:
                print("Warning: null pdftext sent in")
            session_goal = "Today you will talk to the student about the following text, which they have read:\n" + \
               "-----------------\n " + pdftext + "-----------------\n" + \
               " Start by telling the student that you will discuss their reading, then engage in a dialog, \
               asking them questions about it."
        else:
            session_goal = self.read_prompt(goal, prompt_type="goal")

        prompt = intro_txt + " " + persona_txt + " " + \
            language + " " + background + " " + student_description + " " + role_txt + \
            " " + do_not + " " + vocab_txt +  " " +  session_goal

        return prompt
