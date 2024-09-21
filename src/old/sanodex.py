# from vocode import Agent

# class SanoDexAgent(Agent):
#     def __init__(self):
#         self.stage = 0
#         self.user_data = {}
    
#     def handle_input(self, user_input):
#         if self.stage == 0:
#             # Start conversation
#             response = "Hello, welcome to SanoDex. May I know your full name?"
#             self.stage += 1
#         elif self.stage == 1:
#             # Collect name
#             self.user_data['name'] = user_input
#             response = f"Thanks {user_input}. Can I have your date of birth?"
#             self.stage += 1
#         elif self.stage == 2:
#             # Collect date of birth
#             self.user_data['dob'] = user_input
#             response = f"Thanks for that. I've noted your name as {self.user_data['name']} and your date of birth as {self.user_data['dob']}. Is that correct?"
#             self.stage += 1
#         elif self.stage == 3:
#             # Confirmation
#             if "yes" in user_input.lower():
#                 response = "Great! Thank you for confirming."
#             else:
#                 response = "Let's try again. What's your full name?"
#                 self.stage = 1  # Resetting to the name-collection stage
#         elif self.stage == 4:
#             response = f"Okay {user_data['name']}, can what is your insurance provider?"
#             self.stage += 1
#         elif self.stage == 5:
#             response = f"Okay {user_data['name']}, can what is your insurance ID?"
#             self.user_data['payer_name'] = user_input
#         elif self.stage == 6:
#             response = f"Great, do you have a referral?"
#             self.user_data['payer_name'] = user_input
#         # elif self.stage == 7:
#         #     response = f"Great, do you have a referral?"
#         #     self.user_data['payer_name'] = user_input


#         return response

import openai

class SanoDexAgent:
    def __init__(self):
        self.stage = 0
        self.user_data = {}

    def ask_chatgpt(self, prompt):
        # Send input to ChatGPT and get response
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()

    def extract_information(self, user_input):
        # Instruct ChatGPT to handle complex cases and extract data intelligently
        prompt = f"""
        A caller is providing information about themselves. Extract their name and date of birth if provided:
        - If the caller says their name, capture it as 'name'.
        - If the caller mentions their date of birth, capture it as 'dob'.
        Example input: 'My name is John Doe and I was born on March 3, 1995'
        Expected output: name='John Doe', dob='March 3, 1995'
        
        Input: '{user_input}'
        """
        response = self.ask_chatgpt(prompt)
        return response

    def handle_input(self, user_input):
        # Use ChatGPT to extract info in case the input is out of order
        extracted_info = self.extract_information(user_input)
        
        # If the extracted info contains both name and DOB
        if 'name' in extracted_info and 'dob' in extracted_info:
            self.user_data['name'] = extracted_info['name']
            self.user_data['dob'] = extracted_info['dob']
            response = f"Thanks, {self.user_data['name']}. I've noted your date of birth as {self.user_data['dob']}. Is that correct?"
            self.stage = 3  # Skip to confirmation
        elif self.stage == 0:
            response = "Hello, welcome to SanoDex. May I know your full name?"
            self.stage += 1
        elif self.stage == 1:
            # Collect name
            self.user_data['name'] = user_input
            response = f"Thanks {user_input}. Can I have your date of birth?"
            self.stage += 1
        elif self.stage == 2:
            # Collect date of birth
            self.user_data['dob'] = user_input
            response = f"Thanks for that. I've noted your name as {self.user_data['name']} and your date of birth as {self.user_data['dob']}. Is that correct?"
            self.stage += 1
        elif self.stage == 3:
            if "yes" in user_input.lower():
                response = "Great! Thank you for confirming."
            else:
                response = "Let's try again. What's your full name?"
                self.stage = 1
        return response
