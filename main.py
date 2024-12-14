import os
import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# Configuración de Google AI
genai.configure(api_key="AIzaSyAheriSf5COPnerrWrxeL5TaXAqqaNiEZ0")

# Configuración del modelo
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="tunedModels/genesis10-d0usa0bizydm",
  generation_config=generation_config,
  safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  }
)

mostt = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  generation_config=generation_config,
  system_instruction="Eres un modelo que deve repetir todo lo que se le diga tanto en audio como en texto, no deves agregar contenido adicional a lo que transcribas",
  safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  }
)

chat_session = model.start_chat(history=[])
chat_sessionstt = mostt.start_chat(history=[])

print('Iniciado')

# Conexión con el bot
Key = '7833564522:AAH78-QF1xR8xYXDQXNgR5LDiwphL9fR76w'
bot = telebot.TeleBot(Key)

def send(text):
  x = chat_session.send_message(text)
  return x.text


@bot.message_handler(commands=['status'])
def send_url(message):
  inline = InlineKeyboardMarkup()
  button = InlineKeyboardButton("Play", url='https://zucchini-communication-production.up.railway.app')
  inline.add(button)
  bot.reply_to(message, 'Haz click en "Play" para ver el estado del modelo', reply_markup=inline)


@bot.message_handler(content_types=['text'])
def handle_text(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.reply_to(message, send(message.text))

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
  try:
    # Descargar archivo de audio
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Guardar audio temporalmente
    with open('audio_temp.ogg', 'wb') as new_file:
      new_file.write(downloaded_file)

    # Preparar el archivo de audio para Gemini
    with open('audio_temp.ogg', 'rb') as audio_file:
      audio_bytes = audio_file.read()

    # Enviar audio a Gemini para transcripción
    prompt = "Transcribe el siguiente audio. Si es en español, transfórmalo a texto"
    audio_part = {
        'mime_type': 'audio/ogg',
        'data': audio_bytes
    }

    bot.send_chat_action(message.chat.id, 'typing')
    response = mostt.generate_content([prompt, audio_part])

    # Responder con la transcripción dependiendo del tts
    
    bot.reply_to(message, send(response.text))

  except Exception as e:
    bot.reply_to(message, f"Error al procesar el audio: {str(e)}")

# Inicia el bot
bot.polling()
