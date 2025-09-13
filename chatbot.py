from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set.")
client=Groq(api_key=api_key)

print("Hello")

while True:
    user_input=input("You:")
    if user_input.lower() in ["quit","exit","bye"]:
        print("Goodbye")
        break

    print("Chatbot:",end="",flush=True)

    stream=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":"You are a helpful chatbot."},
            {"role":"user","content":user_input}
        ],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content,end="",flush=True)

    print() 