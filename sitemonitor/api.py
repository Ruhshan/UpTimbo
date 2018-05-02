from .models import Site
from .serializers import SiteSerializer
from rest_framework import generics

class SiteListAPI(generics.ListAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        user = self.kwargs['userid']
        return Site.objects.filter(user = int(user))

class SiteUpdateAPI(generics.UpdateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

