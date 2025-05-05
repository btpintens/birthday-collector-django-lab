#from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Birthday
from .serializers import BirthdaySerializer

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