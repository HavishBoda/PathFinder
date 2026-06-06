from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama3-groq-70b-8192-tool-use-preview",
    messages=[
        {"role": "user", "content": "What is EECS 485 at University of Michigan?"}
    ]
)

print(response.choices[0].message.content)

