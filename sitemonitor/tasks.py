from django.utils import timezone
from .models import Site
from celery import task

from messengerplatform.replies import TextReply
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

@task(name="check_and_notify")
def check_and_notify():
    sites = Site.objects.filter(ismonitoring=True, isdeleted=False)

    for site in sites:
        now = timezone.now()
        diff = now - site.created_at
        elapsed = int(diff.total_seconds() / 60)
        interval = int(site.interval/60)
        print("elapsed", elapsed)
        print("Interval", interval)

        if elapsed % interval == 0:
            site_status = poke_the_site(site)
            if site_status["isalive"] != site.isalive:
                text_reply = TextReply(site.user)
                text_reply.set(site_status["message"])
                text_reply.send()
                site.isalive = site_status["isalive"]
                site.save()


def poke_the_site(site):
    req = Request(site.url)
    result = {}
    print("querying:", site.url)
    try:
        response = urlopen(req, timeout=10)
    except HTTPError as e:
        result["message"] = "Hi, I can't access your site: {}!\n{}".format(site.url,e.code)
        result["isalive"] = False
    except URLError as e:
        result["message"] = "Hi, I can't access your site: {}! {}\n{}".format(site.url,e.reason)
        result["isalive"] = False
    else:
        result["message"] = "Great!, your site {} is up and running".format(site.url)
        result["isalive"] = True
    print("found", result)
    return result


#celery -A project worker -l INFO -B