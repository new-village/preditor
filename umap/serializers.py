from rest_framework import serializers

from umap.models import Race


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Race
        fields = ('race_id', 'race_dt', 'place_name', 'title')
