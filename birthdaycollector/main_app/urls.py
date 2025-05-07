from django.urls import path 
from .views import (
    Home, 
    BirthdayList, 
    BirthdayDetail, 
    PartyList, 
    PartyDetail,
    AddPartyToBirthday,
    RemovePartyFromBirthday,
    CreateUserView, 
    LogInView,
    VerifyUserView
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('birthdays/', BirthdayList.as_view(), name='birthday-list'),
    path('birthdays/<int:id>/', BirthdayDetail.as_view(), name='birthday-detail'), 
    path('party/', PartyList.as_view(), name='party'),
    path('party/<int:id>/', PartyDetail.as_view(), name='party-detail'),
    path('birthdays/<int:birthday_id>/add_party/<int:party_id>/', AddPartyToBirthday.as_view(), name='add-party-to-birthday'),
    path('birthdays/<int:birthday_id>/remove_party/<int:party_id>/', RemovePartyFromBirthday.as_view(), name='remove-party-from-birthday'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LogInView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]