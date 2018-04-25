from django.conf.urls import url, include

from .views import SiteAdd
urlpatterns = [
    url(r'add', SiteAdd.as_view()),
]
