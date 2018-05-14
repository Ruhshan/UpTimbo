from django.shortcuts import render
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings
from messengerplatform.receiver import Receiver
from messengerplatform.replies import Reply, TextReply, QuickReply, WebViewReply

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

        messages = Receiver(request).messages

        for m in messages:

            if m.type == "text":
                quick_reply = QuickReply(m.sender, title_text="Hello {}, What can I do for you today".format(m.sender_name))
                quick_reply.add(content_type="text", title="Site's List", payload="view")
                quick_reply.add(content_type="text", title="Add New Site", payload="add")
                quick_reply.send()
            elif m.type == "quick_reply":
                if m.payload == "add":
                    add_site = WebViewReply(m.sender)
                    add_site.set(text="Adding New Site", title="Click to add a new site", url=settings.WEB_VIEW_URL)
                    add_site.send()
                elif m.payload == "view":
                    view_list = WebViewReply(m.sender)
                    view_list.set(text="Your List", title="Click to view your sites list", url=settings.SITE_LIST_URL+m.sender)
                    view_list.send()

        return HttpResponse()