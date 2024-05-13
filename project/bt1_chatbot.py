import time

import requests
from fn_tg_chatbot import get_updates, send_messages, handle_pdf

from fn_chatgpt import create_thread, run_prompt

from fn_db import load_or_initialize_db, save_db, generador_identificador

from my_keys import BOT_API_URL, BOT_TOKEN, ASSISTANT_TOKEN

def main():


    form_petition_message = 'Con base al plan de accion anual que generaste, crea una encuesta dirigida a los trabajadores de la empresa con el objetivo de monitorear el progreso del plan de acción anual que propusiste. Considera que el número de preguntas que propongas debe ser en función del número de recomendaciones que generaste. Por favor asegúrate de generar preguntas de opción múltiple que puedan ser respondidas con las siguientes opciones de respuesta: a) totalmente de acuerdo, b) de acuerdo, c) no tengo criterios para evaluar, d) en desacuerdo, e) totalmente en desacuerdo. Utiliza un lenguaje facil de entender, que no sea muy técnico. Como respuesta tuya quiero solamente un listado de preguntas, no quiero textos o parrafos antes o despues de las preguntas. Dame tu respuesta en el siguiente formato: pregunta1 \\n pregunta2 \\n pregunta3 \\n ... preguntaN'

    threads_path = "nomoreslavery/datasets/chat_threads.json"

    forms_path = "nomoreslavery/datasets/forms.json"

    id_form_gen = generador_identificador(forms_path)


    offset = 0

    threads_db = load_or_initialize_db(threads_path)

    forms_db = load_or_initialize_db(forms_path)

    

    while True: 

        updates = get_updates(offset, BOT_API_URL)

        if updates:

            for update in updates:

                offset = update["update_id"] + 1

                message = update.get('message')

                chat_id = message["chat"]["id"]

                if message and 'document' in message:

                    print("Documento encontrado")

                    user_message = handle_pdf(update, BOT_TOKEN)

                else:

                    user_message = message.get("text", "")
                


                if str(chat_id) in threads_db:

                    hilo_id = threads_db[str(chat_id)]['hilo_id']

                else:

                    hilo_id = create_thread()

                    threads_db[chat_id] = {"hilo_id": hilo_id, "cuestionario": []}

                    save_db(threads_db, threads_path)

                content = run_prompt(hilo_id,user_message, ASSISTANT_TOKEN)

                send_messages(chat_id, content, BOT_TOKEN)


                if 'document' in message:

                    form = run_prompt(hilo_id,form_petition_message, ASSISTANT_TOKEN)

                    print("Formulario recibido:", form)

                    form_id = next(id_form_gen)

                    forms_db[str(form_id)]= list(form.split('\n'))

                    save_db(forms_db, forms_path)

                    send_messages(chat_id, f"Se generó un cuestionario para los trabajadores de la empresa. Por favor, enviales el siguiente link: https://t.me/nomoreslaverybot, el id para que puedan acceder al cuestionario es: {form_id}", BOT_TOKEN)



if __name__ == '__main__':

    main()
