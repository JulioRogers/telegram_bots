import time

import requests
from fn_tg_chatbot import get_updates, send_messages, handle_pdf

from fn_chatgpt import create_thread, run_prompt

from fn_db import load_or_initialize_db, save_db, generador_identificador

from my_keys import BOT_API_URL_3, BOT_TOKEN_3, ASSISTANT_TOKEN2

from fn_stats import get_statistics

def main():

    threads_path = "nomoreslavery/datasets/chat_threads2.json"
    threads_db = load_or_initialize_db(threads_path)

    offset = 0

    while True: 

        updates = get_updates(offset, BOT_API_URL_3)

        if updates:

            for update in updates:

                offset = update["update_id"] + 1

                message = update.get('message')

                chat_id = message["chat"]["id"]

                user_message = message.get("text", "")

                final_message = "responde a la siguiente pregunta: ", user_message, "usando la siguiente información:", get_statistics()
                print(final_message)
                if str(chat_id) in threads_db:

                    hilo_id = threads_db[str(chat_id)]['hilo_id']

                else:

                    hilo_id = create_thread()

                    threads_db[chat_id] = {"hilo_id": hilo_id, "cuestionario": []}

                    save_db(threads_db, threads_path)

                content = run_prompt(hilo_id,user_message, ASSISTANT_TOKEN2)
                print('paso')
                send_messages(chat_id, content, BOT_TOKEN_3)
                print('paso2')


if __name__ == '__main__':

    main()
