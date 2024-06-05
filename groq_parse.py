import os
import telebot
from dotenv import load_dotenv
from groq import Groq
from get_gmail import get_primary_emails

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
                "content": "The content sent to you is an email with 'sender' and 'body' text, return the sender's name and return a summary of the main points of this email into 30 words or less. Do not send 'Here is a 30-word or less summary of the email' prompt. Send the response with 'From: ' the sender's name only on one line, with a line break after, and then the email body summary"
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
    bot.reply_to(message, "Hello I'm the Blipmail bot. Happy to be of service")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def all_other_messages(message):
    # response = get_groq_response(message.text)
    email_list = get_primary_emails()
    for email in email_list:
        response = get_groq_response(email)
        bot.send_message(message.chat.id, str(response))
    print(len(email_list))
    # response = get_groq_response(email_list)
    # bot.send_message(message.chat.id, str(response))

bot.infinity_polling()