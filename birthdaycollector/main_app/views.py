#from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Birthday, Party
from .serializers import BirthdaySerializer, PartySerializer

# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the birthday-collector home route'}
        return Response(content)
    
class BirthdayList(generics.ListCreateAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
    
class BirthdayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        parties_not_associated = Party.objects.exclude(id_in=instance.parties.all())
        parties_serializer = PartySerializer(parties_not_associated, many=True)
        
        return Response({
        'Birthday': serializer.data, 
        'parties_not_associated': parties_serializer.data
    })
    
class PartyList(generics.ListCreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    
class PartyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    lookup_field = 'id'
    
class AddPartyToBirthday(APIView):
    def post(self, request, birthday_id, party_id):
        birthday = Birthday.objects.get(id=birthday_id)
        party = Party.objects.get(id=party_id)
        birthday.parties.add(party)
        return Response({'message': f'Party {party.theme} added to Birthday {birthday.name}'})

class RemovePartyFromBirthday(APIView):
    def post(self, request, birthday_id, party_id):
        birthday = Birthday.objects.get(id=birthday_id)
        party = Party.objects.get(id=party_id)
        birthday.parties.remove(party)
        return Response({'message': f'Party {party.theme} removed from Birthday {birthday.name}'})