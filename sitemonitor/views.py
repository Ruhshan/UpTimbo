from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings
from .models import *
from pprint import pprint

class SiteAdd(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        print("printing request")

        response = render(request, 'sitemonitor/site_form.html')

        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
        else:
            referer = None
        if referer:
            print("adding xfame")
            if 'www.messenger.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.messenger.com/'
            elif 'm.facebook.com' in referer:
                response['X-Frame-Options'] = 'ALLOW-FROM http://m.facebook.com/'
            else:
                response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/'
        return response



    def post(self, request):
        print("in post")
        print(request.body)
        return HttpResponse("Thank u  close the message")

