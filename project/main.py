import time

import requests
from tg_chatbot import get_updates, send_messages, handle_pdf

from chatgpt import create_thread, run_prompt

from db import load_or_initialize_db, save_db, generador_identificador


def main():


    threads_path = "nomoreslavery/datasets/chat_threads.json"

    forms_path = "nomoreslavery/datasets/forms.json"

    id_form_gen = generador_identificador(forms_path)


    offset = 0

    threads_db = load_or_initialize_db(threads_path)

    forms_db = load_or_initialize_db(forms_path)

    

    while True: 

        updates = get_updates(offset)

        if updates:

            for update in updates:

                offset = update["update_id"] + 1

                message = update.get('message')

                chat_id = message["chat"]["id"]

                if message and 'document' in message:

                    print("Documento encontrado")

                    user_message = handle_pdf(update)

                else:

                    user_message = message.get("text", "")
                


                if str(chat_id) in threads_db:

                    hilo_id = threads_db[str(chat_id)]['hilo_id']

                else:

                    hilo_id = create_thread()

                    threads_db[chat_id] = {"hilo_id": hilo_id, "cuestionario": []}

                    save_db(threads_db, threads_path)

                content = run_prompt(hilo_id,user_message)

                send_messages(chat_id, content)


                if 'document' in message:

                    form_petition = 'Con base al plan de accion anual que generaste, crea una encuesta dirigida a los trabajadores de la empresa con el objetivo de monitorear el progreso del plan de acción anual que propusiste. Considera que el número de preguntas que propongas debe ser en función del número de recomendaciones que generaste. Por favor asegúrate de generar preguntas de opción múltiple que puedan ser respondidas con las siguientes opciones de respuesta: a) totalmente de acuerdo, b) de acuerdo, c) no tengo criterios para evaluar, d) en desacuerdo, e) totalmente en desacuerdo. Utiliza un lenguaje facil de entender, que no sea muy técnico. Como respuesta tuya quiero solamente un listado de preguntas, no quiero textos o parrafos antes o despues de las preguntas. Dame tu respuesta en un formato de lista de python. Ejemplo: ["pregunta1", "pregunta2"]'

                    form = run_prompt(hilo_id,form_petition)

                    print("Formulario recibido:", form)

                    #form_id = next(id_form_gen)

                    #forms_db[str(form_id)]= form

                    #save_db(forms_db, forms_path)

                    send_messages(chat_id, f"Se generó un cuestionario para los trabajadores de la empresa. Por favor, enviales el siguiente link: https://t.me/nomoreslaverybot?start=0001 , el id para que puedan acceder al cuestionario es: 0001")



if __name__ == '__main__':

    main()
