from rest_framework import serializers
from core.models import Itineraries, Mentions, Skills, Areas

class ItinerariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itineraries
        fields = ("id", "name")

class MentionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentions
        fields = ("id", "name")

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ("id", "name", "text")

class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = ("id", "name")