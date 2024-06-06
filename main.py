import os
import telebot
from dotenv import load_dotenv
from groq import Groq
from get_gmail import get_primary_emails
import time
from colorama import Fore

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
TG_API_KEY = os.environ.get('TG_API_KEY')


def get_groq_response(content):
    print(Fore.YELLOW + "Querying Groq...")
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                # System prompt to Groq to summarise email content and dictate format of bot response
                "role": "system",
                # "content": "The content sent to you is an email with 'sender' and 'body' text, return the sender's name and return a summary of the main points of this email into 30 words or less. Do not send 'Here is a 30-word or less summary of the email' prompt. Send the response with 'From: ' the sender's name only on one line, with a line break after, and then the email body summary"
                "content": """You are an expert with 20 years at summarizing emails. Only reply to the user with the following format and do not include any responses such as 'here is the 30-word summary' or 'body:', please reply as succinctly as possible in 30 words or less:
                            'From: ' and include the sender's name, followed by a single blank line, it's very important there is only ONE blank line, followed by the email body summary"""
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

# Start message handler
@bot.message_handler(commands=['start', 'help'])
def send_start_help_message(message):
    bot.reply_to(message, "Hello I'm the Blipmail bot. Happy to be of service")

# Any other message handler
@bot.message_handler(func=lambda message: True, content_types=["text"])
def all_other_messages(message):
    print(Fore.GREEN + f"Message received: {message.text}")
    # Any message to the bot that is not '/start' or '/help' will trigger the 30 minute interval to check for emails
    while True:
        # Get email list array
        email_list = get_primary_emails()
        # Loop through emails in array
        for email in email_list:
            try:
                # Send email content to Groq
                response = get_groq_response(email)
                # Bot to send response from Groq
                print(Fore.YELLOW + "Responding with summary")
                bot.send_message(message.chat.id, str(response))
            except:
                bot.send_message(message.chat.id, "Oops, I had an issue reading one of your emails")
        
        time.sleep(1800)

print(Fore.CYAN + "Running in the background...")

bot.infinity_polling()