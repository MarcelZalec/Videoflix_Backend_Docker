from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator as tg
from django.utils.http import urlsafe_base64_decode
from auth_app.models import CustomUserModel
from django.conf import settings
import os

def activate_user(request, uidb64, token):
    """
    Handles account activation via a token and UID encoded in base64.

    - Decodes the user ID
    - Retrieves the user from the database
    - Validates the token
    - Activates the user if not already active
    - Redirects based on outcome
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
        user = None
    if user is not None and tg.check_token(user, token):
        if not user.is_active: 
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated.')
        else:
            messages.info(request, 'Your account is already activated.')
        return redirect(f"{settings.REDIRECT_LANDING}login/")
    else:
        messages.error(request, 'The activation link is invalid!')
        return redirect(f"{settings.REDIRECT_LANDING}")