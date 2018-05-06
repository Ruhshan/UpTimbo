from rest_framework.decorators import permission_classes

from .models import Site
from .serializers import SiteSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class SiteListAPI(generics.ListAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        user = self.kwargs['userid']
        return Site.objects.filter(user=int(user), isdeleted=False)

@permission_classes((AllowAny, ))
class SiteUpdateAPI(generics.UpdateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

