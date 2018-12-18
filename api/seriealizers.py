"""
    Ficheros de serialización de modelos.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from rest_framework import serializers
from core.models import Itineraries, Mentions, Skills, Areas

class ItinerariesSerializer(serializers.ModelSerializer):

    """
        Serialización del modelo Itineraries
    """

    class Meta:
        model = Itineraries
        fields = ("id", "name")

class MentionsSerializer(serializers.ModelSerializer):

    """
        Serialización del modelo Mentions
    """

    class Meta:
        model = Mentions
        fields = ("id", "name")

class SkillsSerializer(serializers.ModelSerializer):

    """
        Serialización del modelo Skills
    """

    class Meta:
        model = Skills
        fields = ("id", "name", "text")

class AreasSerializer(serializers.ModelSerializer):

    """
        Serialización del modelo Areas
    """

    class Meta:
        model = Areas
        fields = ("id", "name")
