from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime, timedelta
import pytz

# Create Gmail instance from simplegmail
gmail = Gmail()

def get_primary_emails():
    print("Fetching emails...")
    # Params to only get emails received in the past day, and only in the 'primary' folder i.e. not spam or promotions folders
    query_params1 = {
        "newer_than": (1, "day"),
        "category": "primary"
    }

    # Get messages that fit the query params
    messages = gmail.get_messages(query=construct_query(query_params1))
    

    # Email array that will be returned
    email_array = []

    for message in messages:
        
        # Get date from email
        time_string = message.date
        # Format date to ISO format
        email_sent_time = datetime.fromisoformat(time_string)

        # Find current time
        current_time = datetime.now(pytz.timezone('Australia/Sydney'))
        # Calculate time difference
        time_diff = abs(email_sent_time - current_time)

        # If email was sent in the last 30 mins, append message to email_array
        if time_diff <= timedelta(minutes=30):
            email_array.append(
                # Email includes sender name and body text
                f"Sender: {message.sender}"
                f"Body: {message.plain}"
            )
    
    print(f"{len(email_array)} new emails detected")
    return email_array

