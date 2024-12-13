import os
import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# AssemblyAI Integration (replace with your API key)
import assemblyai as aai
aai.settings.api_key = "2eb0dda5e55245efb01f56354a47de58"

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

chat_session = model.start_chat(history=[])

print('Iniciado')

# Conexión con el bot
Key = '7833564522:AAH78-QF1xR8xYXDQXNgR5LDiwphL9fR76w'
bot = telebot.TeleBot(Key)

def send(text):
  x = chat_session.send_message(text)
  return x.text

@bot.message_handler(commands=['/start'])
def send_welcome(message):
  bot.reply_to(message, "¡Hola! Puedo responder a mensajes de texto y voz.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.reply_to(message, send(message.text))

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
  try:
    # Download audio file
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Save audio temporarily
    with open('audio_temp.ogg', 'wb') as new_file:
      new_file.write(downloaded_file)

    # Transcribe audio with AssemblyAI
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best, language_code='es')
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(open('audio_temp.ogg', 'rb'))

    # Send transcribed text to the AI
    bot.send_chat_action(message.chat.id, 'typing')
    response = send(transcript.text)

    # Respond with transcription and AI response
    bot.reply_to(message, response)

  except Exception as e:
    bot.reply_to(message, f"Error al procesar el audio: {str(e)}")

# Inicia el bot
bot.polling()
