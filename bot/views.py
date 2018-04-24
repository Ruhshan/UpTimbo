from django.shortcuts import render
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings
from messengerplatform.receiver import Receiver
from messengerplatform.replies import Reply, TextReply, QuickReply

PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
VERIFY_TOKEN = settings.VERIFY_TOKEN

class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        #incoming_payload = json.loads(self.request.body.decode('utf-8'))
        messages = Receiver(request).messages

        for m in messages:
            #print(m.sender_name, m.type)
            #rep = Reply(m.sender)
            if m.type == "text":
                quick_reply = QuickReply(m.sender, title_text="Hello {}, What can I do for you today".format(m.sender_name))
                quick_reply.add(content_type="text", title="View Sites",payload="view")
                quick_reply.add(content_type="text", title="Add New Site", payload="add")
                quick_reply.send()
            elif m.type == "quick_reply":
                if m.payload == "add":
                    text_reply = TextReply(m.sender)
                    text_reply.set(message="New Site will be added")
                    text_reply.send()
                elif m.payload == "view":
                    #TextReply(m.sender).set(message="You will see site list").send()
                    text_reply = TextReply(m.sender)
                    text_reply.set(message="You will see ur sites")
                    text_reply.send()

        return HttpResponse()