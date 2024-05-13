import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from my_keys import BOT_TOKEN_2

forms_path = "nomoreslavery/datasets/forms.json"

# Cargar preguntas de un archivo JSON
with open(forms_path, 'r') as file:
    cuestionarios = json.load(file)

# Opciones de respuestas fijas
opciones_de_respuestas = [
    "a) Totalmente de acuerdo",
    "b) De acuerdo",
    "c) No tengo criterios para evaluar",
    "d) En desacuerdo",
    "e) Totalmente en desacuerdo"
]

mensaje_de_bienvenida = "Bienvenido al bot de cuestionarios. Por favor, envíame el ID del cuestionario."
cuestionario_invalido = "ID de cuestionario no válido. Por favor, intenta de nuevo."
gracias_por_responder = "Gracias por completar el cuestionario."

# Respuestas del usuario almacenadas en memoria
respuestas_usuario = {}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(mensaje_de_bienvenida)

async def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = update.message.text

    if text.isdigit() and text in cuestionarios:
        # Guardar el id del cuestionario para este chat
        respuestas_usuario[chat_id] = {"cuestionario_id": text, "respuestas": {}}
        await enviar_pregunta(update, context, chat_id, 0)
    else:
        await update.message.reply_text(cuestionario_invalido)

async def enviar_pregunta(update: Update, context: CallbackContext, chat_id: int, pregunta_idx: int) -> None:
    preguntas = cuestionarios[respuestas_usuario[chat_id]["cuestionario_id"]]
    pregunta = preguntas[pregunta_idx]
    # Organizar botones en múltiples filas
    botones = [[InlineKeyboardButton(text=opt, callback_data=f"{pregunta_idx}|{opt}")] for opt in opciones_de_respuestas]
    reply_markup = InlineKeyboardMarkup(botones)

    await update.message.reply_text(pregunta, reply_markup=reply_markup)

async def boton_respuesta(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    pregunta_idx, respuesta = query.data.split('|')

    # Guardar respuesta
    preguntas = cuestionarios[respuestas_usuario[chat_id]["cuestionario_id"]]
    pregunta = preguntas[int(pregunta_idx)]
    respuestas_usuario[chat_id]["respuestas"][pregunta] = respuesta

    # Siguiente pregunta o finalizar
    siguiente_idx = int(pregunta_idx) + 1
    if siguiente_idx < len(preguntas):
        await enviar_pregunta(query, context, chat_id, siguiente_idx)
    else:
        await query.message.reply_text(gracias_por_responder)
        # Aquí puedes guardar las respuestas en un archivo o base de datos
        with open('/nomoreslavery/datasets/respuestas.json', 'w') as file:
            json.dump(respuestas_usuario, file, indent=4)

def main() -> None:
    # Crea la aplicación del bot con tu token
    app = Application.builder().token(BOT_TOKEN_2).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(boton_respuesta))

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()