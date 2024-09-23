import openai

class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_openai_response(self, user_text):
        response = openai.Completion.create(
            model="gpt-4",
            prompt=user_text,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
