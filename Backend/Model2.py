# import cohere
# from rich import print # Import the Rich library to enhance terminal outputs.
# from dotenv import dotenv_values # Import dotenv to load environment variables from a .env file

# env_vars = dotenv_values(".env")

# CohereAPIKey = env_vars.get("CohereAPIKey")

# co = cohere.Client(api_key=CohereAPIKey)

# funcs = [
# "general", "realtime", "carrer_recomendation"
# ]

# messages = []

# preamble = """
# You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
# You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to anything about career help. 
# *** Do not answer any query, just decide what kind of query is given to you. ***
# -> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
# -> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
# -> Respond with 'career( query )' if a query is asking for career recomendation like 'what should i do after 12th?', 'what are the best career options for me?', etc. 
# -> Respond with 'career( query )' if a query is asking for career recomendation like 'start career recomendation ', 'can you help me in career recomendation?', 'start proffession recomendation' etc.
# -> Respond with 'career( query )' if a query is asking for career recomendation like 'what is software engineering ?and what are the best career options for me?', 'is cloud computing a good career option for me ?', 'is it a good career option for me ?', etc.

# *** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
# *** Respond with 'genral ( query )' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
# """
# ChatHistory = [
#         {"role": "User", "message": "how are you?"},
#         {"role": "Chatbot", "message": "general how are you?"},
#         {"role": "User", "message": "do you like pizza?"},
#         {"role": "Chatbot", "message": "general do you like pizza?"},
#         {"role": "User", "message": "what are the best career options for me?"},
#         {"role": "Chatbot", "message": "career what are the best career options for me?"},
#         {"role": "User", "message": "can you help me in career recomendation?"},
#         {"role": "Chatbot", "message": "career can you help me in career recomendation?"},
#         {"role": "User", "message": "what is software engineering ?and what are the best career options for me?"},
#         {"role": "Chatbot", "message": "career what is software engineering ?and what are the best career options for me?"},
#         {"role": "User", "message": "is cloud computing a good career option for me ?"},
#         {"role": "Chatbot", "message": "career is cloud computing a good career option for me ?"},
#         {"role": "User", "message": "is it a good career option for me ?"},
#         {"role": "Chatbot", "message": "career is it a good career option for me ?"},
#         {"role": "User", "message": "start career recomendation"},
#         {"role": "Chatbot", "message": "career start career recomendation"},
        
        
# ]

# def FirstLayerDMM(prompt: str = "test"):
#     messages.append( {"role": "user", "content": f"{prompt}"})

#     stream = co.chat_stream(
#         model='command-r-plus', # Specify the Cohere model to use.
#         message=prompt, # Pass the user's query.
#         temperature=0.7, # Set the creativity level of the model.
#         chat_history=ChatHistory, # Provide the predefined chat history for cont
#         prompt_truncation='OFF', # Ensure the prompt is not truncated.
#         connectors=[], # No additional connectors are used.
#         preamble=preamble # Pass the detailed instruction preamble.
#     )

#     response =""

#     for event in stream:
#         if event.event_type == "text-generation":
#             response += event.text 

#     response = response. replace("\n", "")
#     response = response. split(",")

#     response = [i.strip() for i in response]

#     temp = []

#     for task in response:
#         for func in funcs:
#             if task.startswith(func):
#                 temp.append(task)

#     response = temp

#     if "(query)" in response:
#         newresponse = FirstLayerDMM(prompt=prompt)
#         return newresponse 
    
#     else:
        
#         return response 
    
# if __name__== "__main__":
#     while True:
#         print(FirstLayerDMM(input(">>> ")))




import cohere
from rich import print
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

# Ensure API key is available
if not CohereAPIKey:
    raise ValueError("Cohere API key not found. Please check your .env file.")

# Initialize Cohere Client
co = cohere.Client(api_key=CohereAPIKey)

# Recognized function types
funcs = ["career","general", "realtime"]

# Correct chat history format
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "what are the best career options for me?"},
    {"role": "Chatbot", "message": "career what are the best career options for me?"},
]

# Instruction preamble
preamble = """
You are a very accurate Decision-Making Model that classifies queries into:
- 'career' (for any career-related queries)
- 'general' (for chatbot queries)
- 'realtime' (for up-to-date information)
***Primary Objective:to any queries realated career ***if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above, respond with 'general (query)'.

DO NOT answer queries, only classify them.
"""

def FirstLayerDMM(prompt: str, recursion_depth=0):
    if recursion_depth > 3:  # Prevent infinite recursion
        return ["general (error handling)"]

    # Call Cohere API
    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,  # Ensure correct role names
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )

    # Extract response
    response_text = ""
    for event in stream:
        if event.event_type == "text-generation":
            response_text += event.text 

    #print(f"Raw Response: {response_text}")  # Debugging step

    # Process response
    response = [task.strip() for task in response_text.replace("\n", "").split(",")]

    # Filter recognized categories
    filtered_response = [task for task in response if any(task.startswith(f) for f in funcs)]

    if not filtered_response:  # Retry if the response is invalid
        return FirstLayerDMM(prompt, recursion_depth + 1)

    return filtered_response

# Run interactive loop
if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        print(FirstLayerDMM(user_input))