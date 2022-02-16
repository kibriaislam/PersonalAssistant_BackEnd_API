from __future__ import absolute_import
from audioop import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics,status,views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from authentication.api.serializers import RegistrationSerializer,EmailVerificationSerializer
from authentication.api.utils import SendEmail
from authentication.models import User
from authentication.api.utils import SendEmail

from Base.settings import SECRET_KEY

import jwt




class RegistrationView(views.APIView):

    serializer_class = RegistrationSerializer


    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request)
        relative_url = reverse('email-verify')
        absolute_url =  'http://'+current_site.domain +relative_url+'?token='+token
        email_body = "Hi "+ user.username + "'click on the link below to activate your belasea.com's account \n"+ absolute_url
        data = {
            'email_body':absolute_url, 'email_subject':'Verify Your Email'
        }
        SendEmail.send(data)
        return Response(user_data , status = status.HTTP_201_CREATED)

class EmailVerification(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self ,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,SECRET_KEY)
            user = User.objects.get(id = payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"Your Account is activated !"},status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link Expired'}, status = status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'invalid token'}, status = status.HTTP_400_BAD_REQUEST)