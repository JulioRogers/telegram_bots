import requests
import PyPDF2
from io import BytesIO
from my_keys import BOT_API_URL, BOT_TOKEN

prompt_pdf = 'Tomando las recomendaciones dadas para cada seccion, sugiere un plan de acción anual personalizado, desglosado de manera mensual, con el objetivo de implementar las recomendaciones. Por favor enfócate en las secciones cuya respuesta es distinta a “not applicable”. El texto es el siguiente: '

def get_updates(offset):
    params = {"timeout": 100, "offset": offset}
    try:
        response = requests.get(BOT_API_URL, params=params)
        response.raise_for_status()
        return response.json()["result"]
    except requests.RequestException as e:
        print(f"Error al obtener actualizaciones de mensajes: {e}")
        return None

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/{BOT_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, params=params)
    return response

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
                for page_num in range(1):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text = text.replace('\n', ' ')
                        textfinal += text
                prompt_final = prompt_pdf + textfinal
                return prompt_final