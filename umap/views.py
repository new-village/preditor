from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from umap.models import Race
from umap.serializers import RaceSerializer


def index(request):
    # now = datetime.now(pytz.timezone('Asia/Tokyo'))
    # next = Race.objects.filter(race_dt__gte=now).order_by("race_dt").distinct("race_dt").first().race_dt.strftime("%m月%d日")
    return render(request, "index.html", {"sample": "comment"})


class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Race.objects.all().order_by('-race_dt')
    serializer_class = RaceSerializer
