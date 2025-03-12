from Frontend.GUI import (
GraphicalUserInterface,
SetAssistantStatus,
ShowTextToScreen,
TempDirectoryPath,
SetMicrophoneStatus,
AnswerModifier,
QueryModifier,
GetMicrophoneStatus,
GetAssistantStatus )
from Backend.Model import FirstLayerDMM
from Backend.SpeechToText import SpeechRecognition
from Backend.ChatBot import chat_with_bot
from Backend. TextToSpeech import TextToSpeech
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
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search","name of application"]


def ShowDefaultChatIfNoChats():
    File = open(r'Data\ChatLog.json',"r", encoding='utf-8')
    if len(File.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
             file.write("")

        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        chatlog_data = json. load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content' ]}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content' ]}\n"
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'),"r", encoding='utf-8')
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'),"w", encoding='utf-8')
        File.write(result)
        File.close()

def InitialExecution():
        SetMicrophoneStatus("False")
        ShowTextToScreen("")
        ShowDefaultChatIfNoChats()
        ChatLogIntegration()
        ShowChatsOnGUI()

InitialExecution()

def get_prediction():
    """Function to get prediction input from another source."""
    return input("Enter your prediction: ")

def save_prediction_to_file(filename="Prediction_Data.txt", input_func=get_prediction):
    """Appends user input to the file and structures it after 5 entries."""
    
    # Read existing data
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []
    
    # Get new input from provided function
    new_input = input_func()
    lines.append(new_input + "\n")
    
    # Check if 5 entries exist
    if len(lines) >= 5:
        questions = [
            "QES1=\"What are your top interests and passions?\"\n",
            "QES2=\"What skills do you currently have, and what skills do you want to develop??\"\n",
            "QES3=\"Do you prefer hands-on technical work, research & innovation, or leadership & management roles?\"\n",
            "QES4=\"What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?\"\n",
            "QES5=\"What is your long-term vision for your career (5-10 years ahead)??\"\n"
        ]
        
        answers = [f"ANS{i+1}={lines[i]}" for i in range(5)]
        lines = questions + ["\n"] + answers + ["\n"]
    
    # Write back to file
    with open(filename, "w") as file:
        file.writelines(lines)
    
    print("Data successfully saved to", filename)

def clear_file(filename="Prediction_Data.txt"):
    """Clears the content of the specified file."""
    with open(filename, "w") as file:
        file.truncate(0)
    print("File content cleared.")

def load_prediction_data(filename="Prediction_Data.txt"):
    """Loads the content of the prediction file into a variable."""
    try:
        with open(filename, "r") as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print("File not found.")
        return ""
    
def Career_Recomendation():
    
    Initial = "Initializing The Career Recommendation Software."
    initial2 = "Working on it Sir !!"
    ques_1 = "What are your top interests and passions?"
    ques_2 = "What skills do you currently have, and what skills do you want to develop?"
    ques_3 = "Do you prefer hands-on technical work, research & innovation, or leadership & management roles?"
    ques_4 = "What kind of work environment do you thrive in—structured corporate, startup, freelance, or academia?"
    ques_5 = "What is your long-term vision for your career (5-10 years ahead)??"
    intial3 = "Alright , Fetching the Details "
    initial4 = "Recommendation Fetched Successfully"

    SetAssistantStatus("Executing... ")
    ShowTextToScreen(f"{Assistantname} : {Initial}")
    TextToSpeech(Initial)

    SetAssistantStatus("Answering ... ")
    ShowTextToScreen(f"{Assistantname} : {initial2}")
    TextToSpeech(initial2)

    ShowTextToScreen(f"{Assistantname} : {ques_1}")
    TextToSpeech(ques_1)
    
    SetAssistantStatus("Listening ... ")
    ANS_1= SpeechRecognition()
    ShowTextToScreen(f"{Username} : {ANS_1}")
    get_prediction(ANS_1)
    save_prediction_to_file()

    SetAssistantStatus("Answering ... ")
    ShowTextToScreen(f"{Assistantname} : {ques_2}")
    TextToSpeech(ques_2)
    
    SetAssistantStatus("Listening ... ")
    ANS_2= SpeechRecognition()
    ShowTextToScreen(f"{Username} : {ANS_2}")
    get_prediction(ANS_2)
    save_prediction_to_file()

    SetAssistantStatus("Answering ... ")
    ShowTextToScreen(f"{Assistantname} : {ques_3}")
    TextToSpeech(ques_3)
    
    SetAssistantStatus("Listening ... ")
    ANS_3= SpeechRecognition()
    ShowTextToScreen(f"{Username} : {ANS_3}")
    get_prediction(ANS_3)
    save_prediction_to_file()

    SetAssistantStatus("Answering ... ")
    ShowTextToScreen(f"{Assistantname} : {ques_4}")
    TextToSpeech(ques_4)
    
    SetAssistantStatus("Listening ... ")
    ANS_4= SpeechRecognition()
    ShowTextToScreen(f"{Username} : {ANS_4}")
    get_prediction(ANS_4)
    save_prediction_to_file()

    SetAssistantStatus("Answering ... ")
    ShowTextToScreen(f"{Assistantname} : {ques_5}")
    TextToSpeech(ques_5)
    
    SetAssistantStatus("Listening ... ")
    ANS_5= SpeechRecognition()
    ShowTextToScreen(f"{Username} : {ANS_5}")
    get_prediction(ANS_5)
    save_prediction_to_file()

    ShowTextToScreen(f"{Assistantname} : {intial3}")
    TextToSpeech(intial3)
    SetAssistantStatus("Searching... ")
    
    try:
        if __name__ == "__main__":
            chat_with_bot(load_prediction_data())
            SetAssistantStatus("Answering... ")
            ShowTextToScreen(f"{Assistantname} : {initial4}")
            TextToSpeech(initial4)
            
            #if __name__ == "__main__":
               # clear_file()
            return
          
    except Exception as e:
        logging.error(f"Error in fetching Career Recommendation: {e}")
        ShowTextToScreen(f"{Assistantname} : Error in fetching Career Recommendation")
        SetAssistantStatus("Answering ... ")
        TextToSpeech("Error in fetching Career Recommendation")
        if __name__ == "__main__":
            clear_file()
        return
    
def MainExecution():
    SetAssistantStatus("Listening ... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ... ")
    
    if "career" in Query.lower():
        Career_Recomendation()
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
