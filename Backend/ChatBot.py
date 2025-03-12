from groq import Groq
from json import load, dump
import datetime


# Load environment variables from the .env file
#env_vars = dotenv_values(".env")

# Retrieve specific environment variables
Username = "Anonymous"
Assistantname = "WS CUBE Tech"
GROQ_API_KEY = "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"


# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize an empty list to store chat messages
CHAT_LOG_PATH = "Data/ChatLog.json"
messages = []

# System instructions for the chatbot
system_message = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} with real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
system_chatbot = [{"role": "system", "content": system_message}]


def load_chat_log():
    try:
        with open(CHAT_LOG_PATH, "r") as file:
            return load(file)
    except FileNotFoundError:
        return []


def save_chat_log(messages):
    with open(CHAT_LOG_PATH, "w") as file:
        dump(messages, file, indent=4)


def get_realtime_information():
    now = datetime.datetime.now()
    return f"""Please use this real-time information if needed,
Day: {now.strftime('%A')}
Date: {now.strftime('%d')}
Month: {now.strftime('%B')}
Year: {now.strftime('%Y')}
Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds.
"""


def format_answer(answer):
    return "\n".join(line.strip() for line in answer.splitlines() if line.strip())


def chat_with_bot(query):
    global messages
    messages = load_chat_log()

    messages.append({"role": "user", "content": query})

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=system_chatbot + [{"role": "system", "content": get_realtime_information()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
        )

        answer = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                answer += content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        save_chat_log(messages)
        return format_answer(answer)

    except Exception as e:
        print(f"Error: {e}")
        messages = []
        save_chat_log(messages)
        return "An error occurred. Please try again."


if __name__ == "__main__":
    while True:
        user_query = input("Enter Your Question: ")
        print(chat_with_bot(user_query))
