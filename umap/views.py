from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets

from umap.models import Race
from umap.serializers import RaceSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the umap index.")


class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Race.objects.all().order_by('-race_dt')
    serializer_class = RaceSerializer
