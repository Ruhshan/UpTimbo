from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import *
from pprint import pprint
import json
from messengerplatform.replies import TextReply, QuickReply
from .models import Site
class SiteAdd(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        print("printing request")

        response = render(request, 'sitemonitor/site_form.html', {'load_sdk':settings.LOAD_SDK, 'endpoint':settings.WEB_VIEW_URL})

        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
        else:
            referer = None
        if referer:
            if 'www.messenger.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.messenger.com/'
            elif 'm.facebook.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM http://m.facebook.com/'
            else:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/'
        return response

    def post(self, request):
        json_data = json.loads(request.body.decode())

        print(json_data)

        if json_data['objectid']:
            object_id = 567
        else:
            site=Site.objects.create(user=json_data['psid'], name = json_data["name"], url = json_data["url"], interval= json_data["interval"])
            print(site.id)
        data = {"message":"success","interval":json_data["interval"], "objectid":site.id,"url":json_data["url"],"name":json_data["name"]}
        quick_reply = QuickReply(json_data['psid'], title_text="Your site is on monitoring.")
        quick_reply.add(content_type="text", title="View Sites", payload="view")
        quick_reply.add(content_type="text", title="Add New Site", payload="add")
        quick_reply.send()

        return HttpResponse(json.dumps(data), content_type="application/json")


class SiteList(generic.View):
    def get(self, request, userid):
        sites = Site.objects.filter(user=1650306208417146)
        print(sites)
        response = render(request, 'sitemonitor/site_list.html', {'sites':sites})
        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
        else:
            referer = None

        if referer:
            if 'www.messenger.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.messenger.com/'
            elif 'm.facebook.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM http://m.facebook.com/'
            else:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/'
        return response