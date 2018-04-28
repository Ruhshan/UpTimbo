from django.conf.urls import url, include

from .views import SiteAdd, SiteList
urlpatterns = [
    url(r'add', SiteAdd.as_view()),
    url(r'list/(?P<userid>[0-9]+)', SiteList.as_view())
]
