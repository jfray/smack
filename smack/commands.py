import subprocess
import sys

from .msg import Msg
from .models import PhoneNumber, Message
from os.path import expanduser

import logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    filemode='a',
    format='%(name)s - %(levelname)s - %(message)s'
   )

class Commands:

    msg = Msg()

    def __init__(self):

        self.builtin = {
            'help': self.cmd_help,
            'invite': self.cmd_invite,
            'join': self.cmd_join,
            'list': self.cmd_list,
            'mute': self.cmd_mute,
            'private': self.cmd_private,
            'resend': self.cmd_resend,
            'start': self.cmd_start,
            'stop': self.cmd_stop,
            'update': self.cmd_update,
            'who': self.cmd_who
        }

        self.custom = {
            'test': self.cmd_test,
            'random': self.cmd_random
        }

        self.combined = self.builtin.copy()
        self.combined.update(self.custom)

    @classmethod
    def cmd_help(self, resp=None):
        if len(resp['args']) != 1:
            resp['response'] = self.usage()
            self.msg.send(resp)
        else:
            resp['response'] = self.usage(command=resp['args'][0])
            self.msg.send(resp)
            
    @classmethod
    def cmd_invite(self, resp=None):
        if len(resp['args']) != 1:
            self.msg.send(
                    resp['From'],
                    body=self.usage('invite')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where an invite command would be"
                )

    @classmethod
    def cmd_join(self, resp=None):
        if len(resp['args']) != 1:
            return self.msg.send(
                    resp['From'],
                    body=self.usage('join')
                    )
        else:
            user_add = resp['args'][0].lower()
            if len(user_add) > 20:
               return self.msg.send(
                  resp['From'],
                  body=self.usage('join')
               )
            else:
               if User.objects.filter(username=user_add).count() > 0 or \
                     PhoneNumber.objects.filter(
                              number=resp['From']).count() > 0:
                  return self.msg.send(
                        resp['From'],
                        body="You are already registered as %s. "
                        "Use #udpate <nickname> to change your nickname. "
                        "(20 letter maximum)" % user_add
                        )
               
                  u = User.objects.create(username=user_add)
                  pn = PhoneNumber.objects.create(
                        number = resp['From'],
                        owner = u
                        )

                  return self.msg.send(
                        resp['From'],
                        body="User %s has been added with "
                        "phone number %s" % (user_add, resp['From'])
                        )
            

    @classmethod
    def cmd_list(self, resp=None):
        if len(resp['args']) != 0:
            self.msg.send(
                    resp['From'],
                    body=self.usage('list')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a list command would be"
                )

    @classmethod
    def cmd_mute(self, resp=None):
        if len(resp['args']) != 2:
            self.msg.send(
                    resp['From'],
                    body=self.usage('mute')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a mute command would be"
                )

    @classmethod
    def cmd_private(self, resp=None):
        if len(resp['args']) != 1:
            self.msg.send(
                    resp['From'],
                    body=self.usage('private')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a private command would be"
                )

    @classmethod
    def cmd_resend(self, resp=None):
        if len(resp['args']) != 1:
            self.msg.send(
                    resp['From'],
                    body=self.usage('resend')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a resend command would be"
                )

    @classmethod
    def cmd_start(self, resp=None):
        if len(resp['args']) != 0:
            self.msg.send(
                    resp['From'],
                    body=self.usage('start')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a start command would be"
                )

    @classmethod
    def cmd_stop(self, resp=None):
        if len(resp['args']) != 0:
            self.msg.send(
                    resp['From'],
                    body=self.usage('stop')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a stop command would be"
                )
    
    @classmethod
    def cmd_update(self, resp=None):
        if len(resp['args']) != 1:
            self.msg.send(
                    resp['From'],
                    body=self.usage('update')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where an update command would be"
                )

    @classmethod
    def cmd_who(self, resp=None):
        if len(resp['args']) != 0:
            self.msg.send(
                    resp['From'],
                    body=self.usage('who')
                    )
        else:
            self.msg.send(
                    resp['From'],
                    body="This is where a who command would be"
                )

    ## Please add your custom commands below

    @classmethod
    def cmd_random(self, resp=None):
        if len(resp['args']) != 1:
            self.msg.send(
                    resp['From'],
                    body=self.usage('random')
                    )
        else:
            what_type = resp['args'][0]

            result = subprocess.check_output([
                    "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/bin/python3", 
                    expanduser("~/python/bin/random_thing_picker.py"),
                    "--iterations", 
                    "100000",
                    "--name",
                    what_type.capitalize(),
                    "--show-winner",
                    expanduser("~/%s.txt" % what_type)
                ], 
                universal_newlines=True)

            result = str(result)

            output = []
            for line in result.splitlines():
                output.append(line)

            self.msg.send(
                    resp['From'],
                    body="\n".join(output)
                )
    
    @classmethod
    def cmd_test(self, resp=None):
        if len(resp['args']) != 0:
            self.msg.send(
                      resp['From'],
                      body=self.usage('test')
                      )
        else:
            self.msg.send(
                      resp['From'],
                      body="This is where a test command would be"
                      )

    def usage(command=None):
        help_commands = {
            'help': '#help: List help for all commands',
            'help': '#help <command>: List help for specified command',
            'invite': '#invite <phone_number>: Invite a new user via SMS to the phone number provided',
            'join': '#join <nickname>: Join the chat and set your nickname (20 letter max)',
            'list': '#list: List all users in the room',
            'mute': '#mute <nickname> <on|off>: Stop or start receiving messages from this user',
            'private': '#private <on|off>: Make your profile public or private. Default is private',
            'random': '#random <movie|food|mcu|marvel>: Receive a random choice from these topics',
            'resend': '#resend <number>: Resend the previous <number> of messages sent to you',
            'start': '#start: Start receiving messages from this Smack room',
            'stop': '#stop: Stop receiving messages from this Smack room',
            'test': '#test',
            'update': '#update <new_nickname>: Update your nickname (20 letter max)',
            'who': '#who <nickname>: Get information about a user by providing their nickname if the profile is set '
            'to public. Default is private'
            }

        if command:
            if command in help_commands:
                return "Usage: %s" % help_commands[command]
            else:
                return "Invalid command: %s. Text #help for a list of commands." % command
        else:
            return "\n ".join(help_commands.values())
