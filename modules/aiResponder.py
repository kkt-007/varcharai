from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AIResponder:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    def process_command(self, command):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": command}],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing command: {e}"
    
    def image_command(self, command):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=command,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            return f"Error processing command: {e}"
