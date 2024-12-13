"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""
if __name__ == "__main__":
  import os
  import google.generativeai as genai
  from google.generativeai.types import HarmCategory, HarmBlockThreshold
  import telebot

  genai.configure(api_key="AIzaSyAheriSf5COPnerrWrxeL5TaXAqqaNiEZ0")

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="tunedModels/genesis10-d0usa0bizydm",
    generation_config=generation_config,
    safety_settings ={
      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
      HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  print('Inizando ...')
  # conexion con el bot
  Key = '7833564522:AAH78-QF1xR8xYXDQXNgR5LDiwphL9fR76w'
  bot = telebot.TeleBot(Key)

  def send(text):
     x = chat_session.send_message(text)
     return x.text

  @bot.message_handler(commands=['/Start'])  
  def send_welcome(message):  
      bot.reply_to(message, "¡Hola!")  

  @bot.message_handler(func=lambda message: True)  
  def echo_all(message):
      bot.send_chat_action(message.chat.id, 'typing')
      bot.reply_to(message, send(message.text))  

  # Inicia el bot  
  bot.polling()  
