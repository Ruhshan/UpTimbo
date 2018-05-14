from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import *
from pprint import pprint
from .validator import site_validator
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

        haserror, data = site_validator(json_data)
        
        if haserror:
            data['message'] = "error"
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            if data['objectid']:
                site = Site.objects.get(id=int(data['objectid']))
                site.name = data["name"]
                site.url = data["url"]
                site.interval = round(float(data["interval"]))
                site.save()
            else:
                site=Site.objects.create(user=data['psid'], name=data["name"], url=data["url"], interval=round(float(data["interval"])))
                print('saving')

            data['message']='success'
            data['objectid']=site.id

            # quick_reply = QuickReply(site.user, title_text="Your site is on monitoring.")
            # quick_reply.add(content_type="text", title="View Sites", payload="view")
            # quick_reply.add(content_type="text", title="Add New Site", payload="add")
            # quick_reply.send()

            return HttpResponse(json.dumps(data), content_type="application/json")


class SiteList(generic.View):
    def get(self, request, userid):
        sites = Site.objects.filter(user=userid)
        print(sites)
        response = render(request, 'sitemonitor/site_list.html', {'sites':sites, 'endpoint':settings.SITE_DETAIL_URL, 'update_endpoint':settings.WEB_VIEW_URL})
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

class SiteDetail(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    def post(self, request):
        json_data = json.loads(request.body.decode())
        siteid = json_data['siteid']
        site = Site.objects.get(id=int(siteid))
        data = {
            'name': site.name,
            'url': site.url,
            'interval': site.interval,
            'objectid': site.id,
            'monitoring': site.ismonitoring
        }

        return HttpResponse(json.dumps(data), content_type="application/json")