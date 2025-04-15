from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

text = "What is the capital of India?"

response = client.chat.completions.create(
    model="gpt-4o",
    messages= [
        {"role":"user", "content": text}
    ]
)

print(response.choices[0])

print(response.choices[0].message.content)