#from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Birthday, Party
from .serializers import UserSerializer, BirthdaySerializer, PartySerializer

# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the birthday-collector home route'}
        return Response(content)
    
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

class LogInView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user: 
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

   
class BirthdayList(generics.ListCreateAPIView):
    serializer_class = BirthdaySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Birthday.objects.filter(user=user)
    
    def preform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class BirthdayDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BirthdaySerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user = self.request.user
        return Birthday.objects.filter(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        parties_not_associated = Party.objects.exclude(id_in=instance.parties.all())
        parties_serializer = PartySerializer(parties_not_associated, many=True)
        
        return Response({
        'Birthday': serializer.data, 
        'parties_not_associated': parties_serializer.data
    })
        
    def preform_update(self, serializer):
        birthday = self.get_object()
        if birthday.user != self.request.user: 
            raise PermissionDenied({'message': 'you are not to be here'})
        serializer.save()
        
    def preform_destroy(self, instance):
        if instance.user != self.request.user: 
            raise PermissionDenied({'message': 'you are not allowed'})
        instance.delete()
          
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