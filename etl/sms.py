# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC78c054ba0f1375032890fc5b2ca5d77f"
auth_token = "58c00bb2bac2e6f38e7b9aadd8f50cc9"
client = Client(account_sid, auth_token)

message = client.api.account.messages.create(
    to="+6585005351",
    from_="+13214138465",
    body="Hello there!",
    media_url=['https://demo.twilio.com/owl.png',
               'https://demo.twilio.com/logo.png'])
