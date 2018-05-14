from celery import shared_task
from django.utils import timezone
from .models import Site
from celery import task
#@shared_task(name="check_and_notify")
import urllib.request
from messengerplatform.replies import TextReply

@task(name="check_and_notify")
def check_and_notify():
    sites = Site.objects.all()
    diffs = []
    for site in sites:
        now = timezone.now()
        diff = now - site.created_at
        elapsed = int(diff.total_seconds() / 60)
        interval = int(site.interval/60)
        isalive = True
        resp = "Not found"
        try:
            resp = urllib.request.urlopen(site.url, timeout=10).getcode()
        except:
            resp = "not found"
        # if elapsed % interval == 0:
        #     try:
        #         resp = urllib.request.urlopen(site.url, timeout=10).getcode()
        #         isalive = True
        #     except:
        #         isalive = False
        #
        # if site.isalive != isalive:
        #     if isalive == True:
        #         text_reply = TextReply(site.user)
        #         text_reply.set("Your Site {} is now accessible.".format(site.name))
        #         text_reply.send()
        #     else:
        #         text_reply = TextReply(site.user)
        #         text_reply.set("Your Site {} is now unaccessible.".format(site.name, now))
        #         text_reply.send()
        #     site.isalive = isalive
        #     site.save()
        #     #diffs.append("send"+ str(site.url)+ str(resp))
        diffs.append(resp)
    return diffs



# try:
#     print(urllib.request.urlopen("http://uptimbo.herokuapp.com/admin",timeout=10).getcode())
# except:
#     print("nai")