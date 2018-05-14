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
        """
        Delivers the site add form with required configurations in response header
        :param request:
        :return:
        Renderd site add form
        """

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
        """
        Validates new site's data and saves in the database, provides necessary warnings for invalid data
        :param request:
        :return:
        JSON object for added new data or data along with warnings for invalid submission
        """
        json_data = json.loads(request.body.decode())

        haserror, data = site_validator(json_data)
        
        if haserror:
            data['message'] = "error"
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            if data['objectid']:
                #When data has this attribute, it means it is an existing data, thus fields are updates
                site = Site.objects.get(id=int(data['objectid']))
                site.name = data["name"]
                site.url = data["url"]
                site.interval = round(float(data["interval"]))
                site.save()
            else:
                #New data, thus make a new entry
                site=Site.objects.create(user=data['psid'], name=data["name"], url=data["url"], interval=round(float(data["interval"])))
                print('saving')

            data['message']='success'
            data['objectid']=site.id
            #A quick reply so that after adding a new site user can repeat the task prompty
            quick_reply = QuickReply(site.user, title_text="Your site {} is on monitoring.".format(site.name))
            quick_reply.add(content_type="text", title="Sites List", payload="view")
            quick_reply.add(content_type="text", title="Add New Site", payload="add")
            quick_reply.send()

            return HttpResponse(json.dumps(data), content_type="application/json")


class SiteList(generic.View):
    """
    Webview content for sites list
    Todo: Make this restful
    """
    def get(self, request, userid):
        sites = Site.objects.filter(user=userid)
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