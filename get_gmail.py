from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime, timedelta
import pytz

gmail = Gmail()

def get_primary_emails():

    query_params1 = {
        "newer_than": (1, "day"),
        "category": "primary"
    }

    messages = gmail.get_messages(query=construct_query(query_params1))

    # for message in messages:
    #     print("Subject: " + message.subject)

    email_array = []

    for message in messages:
        
        time_string = message.date
        email_sent_time = datetime.fromisoformat(time_string)

        current_time = datetime.now(pytz.timezone('Australia/Sydney'))
        time_diff = abs(email_sent_time - current_time)

        if time_diff <= timedelta(minutes=30):
            email_array.append(
                f"Sender: {message.sender}"
                f"Body: {message.plain}"
            )
    
    return email_array

