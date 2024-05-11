import time
import requests
from telegram import get_updates, send_messages, handle_pdf
from chatgpt import create_thread, run_prompt
from pdftext import texto
from db import load_or_initialize_db, save_db


def main():
    offset = 0
    while True: 
        database = load_or_initialize_db()
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get('message')
                chat_id = message["chat"]["id"]
                if message and 'document' in message:
                    print("Documento encontrado")
                    #user_message = texto
                    user_message = handle_pdf(update)
                else:
                    user_message = message.get("text", "")
                

                if str(chat_id) in database:
                    hilo_id = database[str(chat_id)]['hilo_id']
                else:
                    hilo_id = create_thread()
                    database[chat_id] = {"hilo_id": hilo_id, "cuestionario": []}
                    save_db(database)

                content = run_prompt(hilo_id,user_message)
                send_messages(chat_id, content)

if __name__ == '__main__':
    main()
