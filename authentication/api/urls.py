from django.urls import path
from.views import RegistrationView,EmailVerification
urlpatterns =[

    path('signup/',RegistrationView.as_view(), name = 'registration'),
    path('email-verify/',EmailVerification.as_view(), name = 'email-verify')

]