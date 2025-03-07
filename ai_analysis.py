from google import genai
from datetime import datetime
import pickle
import os

HISTORY = '2025-03-07T12:48:04'
OUR_TEAM_NAME = 'Creek Smash Red Team'
OPP_TEAM_NAME = 'FCHS Smash A'

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

if HISTORY:
    with open(f'history/{HISTORY}', 'w', encoding='UTF-8') as f:
        chat = client.chats.create(history=pickle.loads(f), model="gemini-2.0-flash")
else:
    chat = client.chats.create(model="gemini-2.0-flash")
    
    with open(f'formatted_data/{OUR_TEAM_NAME}', 'r', encoding='UTF-8') as f:
        chat.send_message(f'Here is the match data of our SSBU team:\n{f.read()}')

    with open(f'formatted_data/{OPP_TEAM_NAME}', 'r', encoding='UTF-8') as f:
        chat.send_message(f'Here is the match data of the enemy SSBU team:\n{f.read()}')

while (prompt := input('> ')):
    response = chat.send_message(prompt)
    print(f'\n{response.text}')

DATE = datetime.now().replace(microsecond=0).isoformat()
with open(f'gemini_chat_history/{DATE}', 'xb', encoding='UTF-8') as f:
    pickle.dumps(chat.get_history(), f)
