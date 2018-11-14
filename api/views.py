from rest_framework import generics
from core.models import Itineraries, Mentions, Skills, Areas
from api.seriealizers import ItinerariesSerializer, MentionsSerializer, SkillsSerializer, AreasSerializer

class ListItineraries(generics.ListAPIView):
    queryset = Itineraries.objects.all()
    serializer_class = ItinerariesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(carrers_id=self.kwargs['carrer_id'])
        return queryset

class ListMentions(generics.ListAPIView):
    queryset = Mentions.objects.all()
    serializer_class = MentionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(carrers_id=self.kwargs['carrer_id'])
        return queryset

class ListSkills(generics.ListAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(itineraries_id=self.kwargs['itineraries_id'])
        return queryset

class ListAreas(generics.ListAPIView):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(departaments_id=self.kwargs['departaments_id'])
        return queryset