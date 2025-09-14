import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Test."}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
