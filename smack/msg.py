from twilio.rest import Client
from .worker import Worker

from . import config
import os

class Msg:

    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.environ.get('TWILIO_NUMBER')

    def parse(self, request):

        resp = {}

        # convert the custom type received from Twilio into a usable dictionary
        for key in request.form.keys():
            resp[key] = request.form[key]

        body_parts = request.form['Body'].split()
        if request.form['Body'].startswith(config.COMMAND_IDENTIFIER):
            command = body_parts[0].lstrip(config.COMMAND_IDENTIFIER).lower()
        else:
            command = None

        resp['command'] = command
        resp['args'] = body_parts[1:]

        return resp

    def send(self, to, body):
        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
                body = body,
                from_= self.twilio_number,
                to = to
                )

        return message.sid
