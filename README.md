# Smores 💬
SMS-based chat room, similar-ish to Slack. There's a built-in invite system, muting/unmuting, and it's easily extendable. Have at it!

# Usage 💬
* `#join <nickname>`: Join the chat and set your nickname (20 letter maximum)
* `#update <new nickname>`: Update your nickname (20 letter maximum)
* `#invite <phone number>`: Invite a new user via SMS to the phone number provided
* `#who <nickname>`: Get information about a user by providing their nickname if the profile is set to public. Default is private
* `#private <on|off>`: Make your profile public or private. Default is private
* `#stop`: Stop receiving messages from this Smores room
* `#start`: Start receiving message from this Smores room
* `#list`: List all users in the room
* `#resend <number>`: Resend the previous \<number> of messages sent to you
* `#mute <nickname> <on|off>`: Stop or start receiving messages from this user
* `#admin <nickname> <on|off>`: Enable or disable admin privileges for a given user. Only applicable if you are already an admin.
* `#help`: List help for all commands
* `#help <command>`: List help for command specified

# Requirements 💬
* Publicly addressable machine/VPS/ngrok instance/etc.
* Python 3.7.2
* Redis server installed
 * `brew install redis-server` and follow the instructions to get it to start on boot
 
## Twilio 💬
* This app requires a Twilio account, setup to post to whatever IP/port you've exposed on the server

## Redis Queue for Django (django_rq) 💬
* `python manage.py rqworker` will process whatever is currently in the queue
* `python manage.py rqstats` will provide you information on what's in the queue
* `rq empty <default|failed>` will clear the specified queue
* django_rq is configured via your `smores.settings` file. A minimal configuration looks like this:
  
```    RQ_QUEUES = {
      'default': {
          'HOST': 'localhost',
         'PORT': 6379,
         'DB': 0,
        }
      }
```
* For further configuration options, please refer [here](https://github.com/rq/django-rq#support-for-django-redis-and-django-redis-cache)

## Honcho 💬
* honcho start will start all your services

## Create Database 💬
 * Smores uses the Flango pattern (Flask in the front, Django in the back), as described [here](https://github.com/kennethreitz/flango) by @kennethreitz
 * The traditional `app.py` for Flask is instead `smores/frontend.py`
 * Build the DB by updating `smores/settings.py` with your database connection information, then run `python manage.py migrate --run-syncdb`

## Phonenumber Data Model 💬
* Number: User's phone number, string, length=10 (US Only), 25 (Int'l)
 * Can't be integer because many phone numbers start with 0 (due to country codes)
 * Second pass will be to abstract out country code and phone number
* Owner: ForeignKey to Flask's User/Auth model if possible
* Muted_by: Many to Many with User
* get\_reply\_numbers: Function that returns all phone numbers, excluding your own, excluding any that you have been muted by, and excluding any that are is_active = False
* is_active: Bool default True
* is_private: Bool default True
* is_admin: Bool default False

## Message Model 💬
 * Text: The text of the message sent, string, length=2048 (to allow for multi-part messages)
 * Sid: The delivery ID `SID` received from Twilio upon successful request, string
 * Created At: The time that the message was saved, DateTime

## Data available from Twilio 💬
 * 'ToCountry', 'US'
 * 'ToState', 'CA'
 * 'SmsMessageSid', 'SMb7f1146ce509ee2bc7af12e14ac91143
 * 'NumMedia', '0'
 * 'ToCity', 'MILL VALLEY'
 * 'FromZip', ''
 * 'SmsSid', 'SMb7f1146ce509ee2bc7af12e14ac91143'
 * 'FromState', 'CA'
 * 'SmsStatus', 'received'
 * 'FromCity', ''
 * 'Body', '#test'
 * 'FromCountry', 'US'
 * 'To', '+14158776225'
 * 'ToZip', '94941'
 * 'NumSegments', '1'
 * 'MessageSid', 'SMb7f1146ce509ee2bc7af12e14ac91143'
 * 'AccountSid', 'ACdd5eac9075d080bd7c50819cbf25b64b'
 * 'From', '+15107755852'
 * 'ApiVersion', '2010-04-01'


## Roadmap Stuff

 * Rules engine that has access to Twilio data
  * `if sms.SmsStatus == 'recieved': do.something(interesting)`
 * Update get\_reply\_numbers with more performant fanout
 * Package this as Dockerfile, with appropriate network config
 * Migrate custom commands to external API
  * Create admin screen to add new commands
 * Script phone number/shortcode provisioning and Twilio config
