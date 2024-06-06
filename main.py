import os
import telebot
from dotenv import load_dotenv
from groq import Groq
from get_gmail import get_primary_emails
import time
from colorama import Fore, Style

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
                "content": "You will be sent email content. Please create a single paragraph summary in 30 words or less. Never include phrases such as 'Here is the body summary' or similary wording before the summary. Please use the following message format to reply:'From: ' and include the sender's name, followed by a single blank line, followed by the email body summary."
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
                print(Fore.YELLOW + "Responding with summary" + Style.RESET_ALL)
                bot.send_message(message.chat.id, str(response))
            except:
                bot.send_message(message.chat.id, "Oops, I had an issue reading one of your emails")
        print(Fore.CYAN + "Going to sleep for the next 30 minutes, goodnight..." + Style.RESET_ALL)
        time.sleep(1800)

print(Fore.CYAN + "Running in the background...")

bot.infinity_polling()