#!/usr/bin/env python

from flask import Flask, request, redirect, render_template, g
from redis import Redis
from rq import Queue
from twilio.twiml.messaging_response import MessagingResponse
from .commands import Commands
from .message import Message

import logging
from . import config

app = Flask(__name__)

c = Commands()
q = Queue(connection=Redis())
m = Message()

@app.route("/", methods=['GET'])
def index():
    return ("Commands are: %s%s" % (config.COMMAND_IDENTIFIER, ", #".join(c.combined.keys())), 200)

@app.route("/txt/sync", methods=['POST'])
def process_sync():
    """Respond to incoming sms with a simple text message"""

    # Start the TwiML response
    resp = MessagingResponse()

    # Add message to response
    resp.message("This is a default message for synchronous sms.")

    return str(resp)

@app.route("/txt/async", methods=['POST'])
def process_async():
    resp = m.parse(request)
    command = resp['command']
    q.enqueue(c.combined[command], resp)
    logging.info("Enqueued: %s" % command)

    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
