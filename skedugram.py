import os
import telebot
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
TG_API_KEY = os.environ.get('TG_API_KEY')

def get_groq_response(content):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a resume writer that has 20 years experience, help the user improve their resume points"
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )

    return str((chat_completion.choices[0].message.content))

bot = telebot.TeleBot(TG_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_start_help_message(message):
    bot.reply_to(message, "Hello I'm the skedugram bot")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def all_other_messages(message):
    response = get_groq_response(message.text)
    bot.send_message(message.chat.id, str(response))

bot.infinity_polling()