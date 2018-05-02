from django.conf.urls import url, include

from .views import SiteAdd, SiteList,SiteDetail
from .api import SiteListAPI, SiteUpdateAPI
urlpatterns = [
    url(r'api/v1/list/(?P<userid>[0-9]+)',SiteListAPI.as_view()),
    url(r'api/v1/update/(?P<pk>[0-9]+)',SiteUpdateAPI.as_view()),
    url(r'add', SiteAdd.as_view()),
    url(r'list/(?P<userid>[0-9]+)', SiteList.as_view()),
    url(r'sitedetail/', SiteDetail.as_view()),

]
