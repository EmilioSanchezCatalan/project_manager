"""
    Controladores de la api

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from rest_framework import generics
from core.models import Itineraries, Mentions, Skills, Areas
from api.seriealizers import ItinerariesSerializer, MentionsSerializer
from api.seriealizers import AreasSerializer, SkillsSerializer

class ListItineraries(generics.ListAPIView):

    """
        Controlador para listar los Itinerarios en formato json

        Atributos:
            queryset(Queryset): listado de itinerarios
            serializer_class(models.Model): Modelo que serializar
    """

    queryset = Itineraries.objects.all()
    serializer_class = ItinerariesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(carrers_id=self.kwargs['carrer_id'])
        return queryset

class ListMentions(generics.ListAPIView):

    """
        Controlador para listar las Menciones en formato json

        Atributos:
            queryset(Queryset): listado de meciones
            serializer_class(models.Model): Modelo que serializar
    """

    queryset = Mentions.objects.all()
    serializer_class = MentionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(carrers_id=self.kwargs['carrer_id'])
        return queryset

class ListSkills(generics.ListAPIView):

    """
        Controlador para listar las competencias en formato json

        Atributos:
            queryset(Queryset): listado de competencias
            serializer_class(models.Model): Modelo que serializar
    """

    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(itineraries_id=self.kwargs['itineraries_id'])
        return queryset

class ListAreas(generics.ListAPIView):

    """
        Controlador para listar las areas en formato json

        Atributos:
            queryset(Queryset): listado de areas
            serializer_class(models.Model): Modelo que serializar
    """

    queryset = Areas.objects.all()
    serializer_class = AreasSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(departaments_id=self.kwargs['departaments_id'])
        return queryset
