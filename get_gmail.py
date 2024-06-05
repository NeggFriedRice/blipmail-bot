from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime

gmail = Gmail()

def get_primary_emails():
    labels = gmail.list_labels()

    query_params1 = {
        "newer_than": (1, "day"),
        "category": "primary"
    }

    messages = gmail.get_messages(query=construct_query(query_params1))

    # for message in messages:
    #     print("Subject: " + message.subject)
    time = messages[0].date.split("")
    print(messages[0].date)