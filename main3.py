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
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
                    f.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as f:
                    f.write(DefaultMessage)
    except FileNotFoundError:
        logging.error("ChatLog.json not found. Creating new default logs.")
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
            f.write("")
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as f:
            f.write(DefaultMessage)

def ReadChatLogJson():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.error("Error reading ChatLog.json")
        return []

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""

    for entry in json_data:
        role = Username if entry["role"] == "user" else Assistantname
        formatted_chatlog += f"{role}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            Data = file.read()

        if Data:
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(Data)
    except FileNotFoundError:
        logging.error("Database.data not found.")

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def safe_speech_recognition():
    try:
        return SpeechRecognition()
    except Exception as e:
        logging.error(f"Speech recognition error: {e}")
        return "I couldn't understand that."

def save_prediction_to_file(filename="Prediction_Data.txt", input_text=""):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    if input_text:
        lines.append(input_text + "\n")

    if len(lines) >= 5:
        questions = [
            'QES1="What are your top interests and passions?"\n',
            'QES2="What skills do you currently have, and what skills do you want to develop?"\n',
            'QES3="Do you prefer hands-on technical work, research & innovation, or leadership & management roles?"\n',
            'QES4="What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?"\n',
            'QES5="What is your long-term vision for your career (5-10 years ahead)?"\n'
        ]
        answers = [f"ANS{i+1}={lines[i]}" for i in range(5)]
        lines = questions + ["\n"] + answers + ["\n"]

    with open(filename, "w", encoding='utf-8') as file:
        file.writelines(lines)

def clear_file(filename="Prediction_Data.txt"):
    with open(filename, "w", encoding='utf-8') as file:
        file.truncate(0)

def load_prediction_data(filename="Prediction_Data.txt"):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("Prediction_Data.txt not found.")
        return ""

def Career_Recomendation():
    prompts = [
        "What are your top interests and passions?",
        "What skills do you currently have, and what skills do you want to develop?",
        "Do you prefer hands-on technical work, research & innovation, or leadership & management roles?",
        "What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?",
        "What is your long-term vision for your career (5-10 years ahead)?"
    ]

    ShowTextToScreen(f"{Assistantname}: Initializing The Career Recommendation Software.")
    TextToSpeech("Initializing The Career Recommendation Software.")

    for question in prompts:
        ShowTextToScreen(f"{Assistantname}: {question}")
        TextToSpeech(question)

        SetAssistantStatus("Listening ... ")
        response = safe_speech_recognition()

        ShowTextToScreen(f"{Username}: {response}")
        save_prediction_to_file(input_text=response)

    ShowTextToScreen(f"{Assistantname}: Fetching the details...")
    TextToSpeech("Fetching the details.")

    try:
        recommendation = chat_with_bot(load_prediction_data())
        ShowTextToScreen(f"{Assistantname}: {recommendation}")
        TextToSpeech(recommendation)
        clear_file()  
    except Exception as e:
        logging.error(f"Error in fetching Career Recommendation: {e}")
        ShowTextToScreen(f"{Assistantname}: Error in fetching Career Recommendation")
        TextToSpeech("Error in fetching Career Recommendation")
        clear_file()

def MainExecution():
    SetAssistantStatus("Listening ... ")
    Query = safe_speech_recognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking ... ")

    if "career" in Query.lower():
        Career_Recomendation()
    else:
        response = chat_with_bot(QueryModifier(Query))
        ShowTextToScreen(f"{Assistantname}: {response}")
        SetAssistantStatus("Answering ... ")
        TextToSpeech(response)

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()

        if "Available ... " in AIStatus:
            sleep(0.1)
        else:
            SetAssistantStatus("Available ... ")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    comm.exit_signal.connect(lambda: os._exit(1))
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
