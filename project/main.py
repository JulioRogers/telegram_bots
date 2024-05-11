import json
import base64
from openai import OpenAI
import time
import requests
import PyPDF2
from io import BytesIO
from pdftext import texto
from my_keys import BOT_API_URL, BOT_TOKEN, OPENAI_API_KEY, ASSISTANT_TOKEN

client = OpenAI(api_key=OPENAI_API_KEY)

def get_updates(offset):
    params = {"timeout": 100, "offset": offset}
    try:
        response = requests.get(BOT_API_URL, params=params)
        response.raise_for_status()
        return response.json()["result"]
    except requests.RequestException as e:
        print(f"Error al obtener actualizaciones de mensajes: {e}")
        return None

def send_messages(chat_id,text):
    url = f"https://api.telegram.org/{BOT_TOKEN}/sendMessage"
    params = {"chat_id": chat_id,"text":text}
    response = requests.post(url,params=params)
    return response

def create_thread(prompt_textplain):
    try:
        thread = client.beta.threads.create()
        print("Thread ID:", thread)
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content='dime algo acerca de esto : ' + prompt_textplain,
        )
        
        return thread.id
    
    except Exception as e:
        print("Error al crear hilo y mensaje:", e)
        return None

    
def run_prompt(thread_id): 
    try: 
        run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=ASSISTANT_TOKEN 
            )

        while True:
            try:
                keep_retrieving_run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                if keep_retrieving_run.status == 'failed':
                    print("\nLa ejecución ha fallado.")
                    print("Error Message keep_retrieving_run: ", keep_retrieving_run.last_error.message)
                    raise RuntimeError("La ejecución ha fallado.")

                if keep_retrieving_run.status == "completed":
                    print("\nLa ejecución ha sido completada.")
                    break
                else:
                    time.sleep(5)
            except Exception as e:
                print("Error al recuperar la ejecución:", e)
                raise RuntimeError("Error al recuperar la ejecución.")
            


        response_openai = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        if response_openai.data:
            if response_openai.data[0].content:
                content = response_openai.data[0].content
                response = content[0].text.value
                return response
            else:
                print("No hay contenido en el 'response_openai.data' list.")
        else:
            print("No hay contenido en el 'response_openai' list.")

    except Exception as e:
        print("Error en la funcion run_prompt:", e)
        raise RuntimeError("Error run_prompt function")

def handle_pdf(update):
    message = update.get('message')
    if message and 'document' in message:
        document = message['document']
        if document['mime_type'] == 'application/pdf':
            file_id = document['file_id']
            file_name = document['file_name']
            file_path = f"https://api.telegram.org/{BOT_TOKEN}/getFile?file_id={file_id}"
            response = requests.get(file_path)
            if response.ok:

                file_path = response.json()['result']['file_path']
                download_url = f"https://api.telegram.org/file/{BOT_TOKEN}/{file_path}"
                pdf_response = requests.get(download_url)
                pdf_file = BytesIO(pdf_response.content)
                reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(reader.pages)
                textfinal = ''
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text = text.replace('\t', ' ')
                        textfinal += text
                    textfinal+= '\n'
                print(textfinal)

def main():
    offset = 0
    while True: 
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get('message')
                chat_id = message["chat"]["id"]
                if message and 'document' in message:
                    print("Documento encontrado")
                    #user_pdf = handle_pdf(update)
                    user_pdf = texto
                    user_message = "dame un plan de accion de 12 meses para realizar las mejoras se sugieren a continuan: " + user_pdf
                else:
                    user_message = message["text"]
                
                hilo_id =create_thread(user_message)
                content = run_prompt(hilo_id)
                send_messages(chat_id,content)

if __name__ == '__main__':
    main()