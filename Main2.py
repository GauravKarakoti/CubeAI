from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.SpeechToText import SpeechRecognition
from Backend.ChatBot import chat_with_bot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import logging
import os
from PyQt5.QtCore import pyqtSignal, QObject

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Communicate(QObject):
    exit_signal = pyqtSignal()

comm = Communicate()

env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
DefaultMessage = f"""{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I help you?"""
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search", "name of application"]

def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
            content = file.read()
        
        if len(content) < 5:
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write("")
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)
    except FileNotFoundError:
        logging.warning("ChatLog.json file not found. Creating default chat.")

def ReadChatLogJson():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = "\n".join(
        f"{Username if entry['role'] == 'user' else Assistantname}: {entry['content']}"
        for entry in json_data
    )
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            data = file.read()
        
        if data:
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(data)
    except FileNotFoundError:
        logging.warning("Database.data file not found.")

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def save_prediction_to_file(filename="Prediction_Data.txt", input_func=input):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []
    
    new_input = input_func()
    lines.append(new_input + "\n")
    
    if len(lines) >= 5:
        questions = [
            "QES1=\"What are your top interests and passions?\"\n",
            "QES2=\"What skills do you currently have, and what skills do you want to develop?\"\n",
            "QES3=\"Do you prefer hands-on technical work, research & innovation, or leadership & management roles?\"\n",
            "QES4=\"What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?\"\n",
            "QES5=\"What is your long-term vision for your career (5-10 years ahead)?\"\n"
        ]
        answers = [f"ANS{i+1}={lines[i]}" for i in range(5)]
        lines = questions + ["\n"] + answers + ["\n"]
    
    with open(filename, "w") as file:
        file.writelines(lines)

def load_prediction_data(filename="Prediction_Data.txt"):
    """Loads the content of the prediction file into a variable."""
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        logging.error("Prediction file not found.")
        return ""

def Career_Recommendation():
    prompts = [
        "Initializing The Career Recommendation Software.",
        "Working on it!", 
        "Fetching the Details", 
        "Recommendation Fetched Successfully"
    ]
    
    for text in prompts[:2]:
        SetAssistantStatus("Executing...")
        ShowTextToScreen(f"{Assistantname} : {text}")
        TextToSpeech(text)
    
    questions = [
        "What are your top interests and passions?",
        "What skills do you currently have, and what skills do you want to develop?",
        "Do you prefer hands-on technical work, research & innovation, or leadership & management roles?",
        "What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?",
        "What is your long-term vision for your career (5-10 years ahead)?"
    ]
    
    for question in questions:
        ShowTextToScreen(f"{Assistantname} : {question}")
        TextToSpeech(question)
        answer = SpeechRecognition()
        ShowTextToScreen(f"{Username} : {answer}")
        save_prediction_to_file(input_func=lambda: answer)
    
    ShowTextToScreen(f"{Assistantname} : {prompts[2]}")
    TextToSpeech(prompts[2])
    chat_with_bot(load_prediction_data())
    ShowTextToScreen(f"{Assistantname} : {prompts[3]}")
    TextToSpeech(prompts[3])

def MainExecution():
    SetAssistantStatus("Listening ... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ... ")
    
    if "career" in Query.lower():
        Career_Recommendation()
    else:
        response = chat_with_bot(QueryModifier(Query))
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ... ")
        TextToSpeech(response)

def FirstThread():
    while True:
        if GetMicrophoneStatus() == "True":
            MainExecution()
        sleep(0.1)

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    comm.exit_signal.connect(lambda: os._exit(1))
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
