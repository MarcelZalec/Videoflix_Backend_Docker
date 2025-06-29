from datetime import timedelta
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from core import settings
from django.contrib.auth import get_user_model, tokens
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone, http
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import *
from auth_app.models import PasswordReset
import os

from django.core.mail import send_mail

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Authenticate the user and return an auth token if credentials are valid.
        """
        serializer = LoginSerializer(data = request.data)
        data = {}
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'remember': user.remember,
                'email': user.email
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Register a new user and return an auth token.
        """
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user = saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPassowrdResetView(APIView):
    permission_classes = [AllowAny]
    TokenAuthentication = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        """
        Generates a password reset token and sends a reset link via email.
        """
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()
            
            reset_url = reverse('reset_password_token', kwargs={'token': token})
            relative_reset_url = reset_url.replace('/api', 'api')
            custom_port_url = f'{settings.REDIRECT_LANDING}resetPassword/{token}'
            full_url = custom_port_url
            domain_url = os.getenv(f'{settings.REDIRECT_LANDING}/resetPassword')
            subject = "Reset your password"
            text_content = render_to_string('emails/forgot_password.txt', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            html_content = render_to_string('emails/forgot_password.html', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.attach_alternative(html_content, "text/html")
            ## print(email.message())
            email.send(fail_silently=False)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    permission_classes = []
    
    def get(self, request, token):
        """
        Validates the reset token and checks expiration.
        """
        obj = PasswordReset.objects.filter(token=token).first()
        if not obj:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_lifetime = timedelta(hours=24)
        if timezone.now() > obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Token is valid'}, status=status.HTTP_200_OK)
    
    def post(self, request, token):
        """
        Updates the user's password if the token is valid.
        """
        obj = PasswordReset.objects.filter(token=token).first()
        if not obj:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_lifetime = timedelta(hours=24)
        if timezone.now() > obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=obj.email).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
            obj.delete()
            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)


class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Confirms whether the provided token matches the authenticated user's token.
        """
        sended_Token = request.data.get('token')
        user_token  = request.auth
        
        if sended_Token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)