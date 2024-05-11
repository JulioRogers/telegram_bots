import time
import requests
from telegram import get_updates, send_messages, handle_pdf
from chatgpt import create_thread, run_prompt
from pdftext import texto


def main():
    offset = 0
    while True: 
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get('message')
                if message:                
                    chat_id = message["chat"]["id"]
                if message and 'document' in message:
                    print("Documento encontrado")
                    user_pdf = handle_pdf(update)
                    #user_pdf = texto
                    user_message = user_pdf
                else:
                    user_message = message["text"]
                

                hilo_id = create_thread(user_message)
                content = run_prompt(hilo_id)
                send_messages(chat_id, content)

if __name__ == '__main__':
    main()
