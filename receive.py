import os
from flask import Flask, request, Response, render_template
from slackclient import SlackClient
from app import send_message, list_channels, channel_info, get_convo
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

slack_client = SlackClient(SLACK_TOKEN)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

@app.route('/twilio', methods=['POST'])
def twilio_post():
    response = MessagingResponse()
    if request.form['From'] == USER_NUMBER:
        message = request.form['Body']
        slack_client.api_call("chat.postMessage", channel="#general",
                              text=message, username='tbot',
                              icon_emoji=':robot_face:')
    return Response(response.toxml(), mimetype="text/xml"), 200

@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:

        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')

        inbound_message = username + " in " + channel + " says: " + text
        message_history = []
        if not message_history:
            message_history = []

        print(inbound_message)

        message_history.append(inbound_message)


        channels = list_channels()

        game_topics = ['a: guess a word', 'b: run a test', 'c: release the monkey']
        monkey_topics = ['a: chimpanzee', 'b: ape', 'c: baboon']

        for c in channels:
            detailed_info = channel_info(c['id'])
            if c['name'] == 'general':
                general_channel = c['id']

        if text == 'play a game':
            for t in game_topics:
                send_message(general_channel, t)
        if text == 'hi':
            send_message(general_channel, "Hey")
        if text == 'what are you doing':
            send_message(general_channel, "Watching TV")
        if text == 'what should i do tonight':
            send_message(general_channel, "make a cake")
        if text == 'c':
            for m in monkey_topics:
                send_message(general_channel, m)
            print message_history
        else:
            print("Unable to authenticate.")

    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    print get_convo()
    channels = list_channels()
    return render_template('main.html', content=channels)


if __name__ == "__main__":
    app.run(debug=True)
