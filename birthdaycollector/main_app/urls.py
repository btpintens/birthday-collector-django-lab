from django.urls import path 
from .views import Home, BirthdayList, BirthdayDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('birthdays/', BirthdayList.as_view(), name='birthday-list'),
    path('birthdays/<int:id>/', BirthdayDetail.as_view(), name='birthday-detail'), 
]