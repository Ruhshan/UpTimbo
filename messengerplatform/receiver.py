import json
from django.conf import settings
import requests
PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
VERIFY_TOKEN = settings.VERIFY_TOKEN

from pprint import pprint
class Message():
    """
    A object oriented representation of incoming messages

    Args:
        data (dict): Json parsed dictinary
    Attributes:
        data (dict): received data dictionary
        sender (str): sender id
        recipient (str): recipient id
        timestamp (str): unix timestamp
        type (str): message type
        text (str): text for text type message
        payload (str): payload for quick reply
        sender_name (str): sender's name

    """
    def __init__(self, data):
        self.data = data
        self.sender = data['sender']['id']
        self.recipient = data['recipient']['id']
        self.timestamp = data['timestamp']
        self.type = self.__get_type()
        self.text = None
        self.payload = None
        self.__user_detail = self.__get_user_details()
        self.sender_name = self.__user_detail['first_name'] +' '+ self.__user_detail['last_name']
        if self.type=='text':
            try:
                self.text = data['message']['text']
            except:
                pass
        elif self.type == "quick_reply":
            try:
                self.payload = data['message']['quick_reply']['payload']
            except:
                pass

    def __get_user_details(self):
        user_details_url = "https://graph.facebook.com/v2.6/%s" % self.sender
        user_details_params = {'fields': 'first_name,last_name,profile_pic',
                               'access_token': PAGE_ACCESS_TOKEN}
        user_details = requests.get(user_details_url, user_details_params).json()

        return user_details

    def print_data(self):
        pass

    def __get_type(self):
        try:
            if 'quick_reply' in self.data['message'].keys():
                return 'quick_reply'
            else:
                return 'text'
        except:
            return "delivery"

class Receiver():
    """
    It takes a request objects and makes the messages available for easy use
    """

    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body.decode('utf-8'))
        self.entry_id = self.data['entry'][0]['id']
        self.__messaging = [event['messaging'] for event in self.data['entry']]
        self.messages=self.__parse_messages()

    def printdata(self):
        print(self.entry_id)
        print(self.messages)

    def __parse_messages(self):
        message_objects = []
        for messages in self.__messaging:

            for m in messages:
                message = Message(m)
                message_objects.append(message)

        return message_objects


