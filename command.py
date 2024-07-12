import os
import time
from Model import GeminiTranscript
from rich.console import Console
from rich.markdown import Markdown
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('Gemini Personal Chat!')
logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler('application.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

os.system('cls')
console = Console()
GeminiModel = GeminiTranscript()
def save_log(texts: list[str]):
    try:
        os.makedirs('./ChatHistory')
    except FileExistsError:
        pass
    path = f'./ChatHistory/{int(time.time())}.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts).strip())
    print(f'Chat History saved to: \'{path}\'')

def user_input():
    noti = '# **Do you want to exit? (Y/N)?**'
    chat_history.append(f'System: {noti}')
    logger.info(chat_history[-1])
    console.print(Markdown(noti))
    check = input().upper()
    chat_history.append(f'User: {check}')
    logger.info(chat_history[-1])
    return check

def confirm_exit():
    check = user_input()
    while check != 'Y' and check != 'N':
        retry_message = '# **Please retype!**'
        chat_history.append(retry_message)
        logger.info(chat_history[-1])
        console.print(Markdown(retry_message))
        check = user_input()
    return check == 'Y'

def model_respone(user_prompt):
    wait_message = '# **Wait for response!**'
    console.print(Markdown(wait_message))
    response = GeminiModel.respone(user_prompt, 'Always respone in Markdown type') 
    console.print(Markdown(response))
    chat_history.append(f'\n{"=" * 5}\nAI respone: {response}\n{"=" * 5}')
    logger.info(chat_history[-1])
    
AI_chat_first_chat = 'Hello, I\'m Grizmo\'s Gemini model! How can I help you today?'
# chat_history = [display_info]
logs = []
chat_history = ['System: ' + AI_chat_first_chat]
logger.info(chat_history[-1])
print(AI_chat_first_chat + '\n')

while True:
    user_prompt = input('\n\nRequest: ')
    chat_history.append(f'User: {user_prompt}')
    if user_prompt.lower() == 'exit':
        exit_message = 'Exit chat mode!'
        chat_history.append(exit_message)
        print(exit_message)
        break
    elif 'exit' in user_prompt.lower():
        if confirm_exit():
            break
        else:
            while True:
                try:
                    model_respone(user_prompt)
                except Exception as e:
                    logger.error(e)
                    model_respone(user_prompt)
    else:
        try:
            model_respone(user_prompt)
        except Exception as e:
            logger.error(e)
            model_respone(user_prompt)

save_log(chat_history)