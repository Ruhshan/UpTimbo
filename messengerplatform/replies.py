import json
import requests
from pprint import pprint
from django.conf import settings

CONTENT_TYPE = {
    'quick_reply': ['text', 'location', 'user_phone_number', 'user_email']
}

class Reply:
    def __init__(self, recipient):
        self.recipient = recipient
        self.params = {
            "access_token": settings.PAGE_ACCESS_TOKEN
            }

        self.headers = {
            "Content-Type": "application/json"
            }

    def _send(self, message):
        data = json.dumps({
            "recipient": {
                "id": self.recipient
            },
            "message": message
        })

        pprint(data)
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=self.params, headers=self.headers, data=data)
        print(r.status_code)
        print(r.text)
        if r.status_code != 200:
            print("Jhamelaaaaaa")



class TextReply(Reply):
    def set(self, message):
        self.message = {"text":message}

    def send(self):
        self._send(self.message)


class QuickReply(Reply):
    def __init__(self, recipient, title_text):
        self.title_text = title_text
        self.quick_replies = []
        super(QuickReply, self).__init__(recipient)


    def add(self, content_type, title=None, payload=None, image_url=None):
        if content_type not in CONTENT_TYPE['quick_reply']:
            raise ValueError(
                "content_type should be one of them ['text', 'location', 'user_phone_number', 'user_email']")
        if content_type == 'text' and (not title or not payload):
            raise ValueError(
                "for text content_type title and payload required")

        quick_reply = {
            "content_type":content_type,
            "title":title,
            "payload":payload,
            "image_url":image_url
        }
        self.quick_replies.append(quick_reply)



    def send(self):
        quick_reply = {"text":self.title_text, "quick_replies":self.quick_replies}
        pprint(quick_reply)
        print(type(quick_reply))
        self._send(quick_reply)

"""
qr = QuickReply(rec)
qr.addreply("dasfdfaf")
qr.addreply("adfadf")
qr.addreply("ddfafaf")

qr.send()


"""