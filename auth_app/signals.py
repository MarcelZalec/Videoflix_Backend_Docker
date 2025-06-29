from auth_app.models import CustomUserModel
from django.dispatch import receiver
from django.db.models.signals import post_save

from core import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator as PRTG
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import get_connection


@receiver(post_save, sender=CustomUserModel)
def user_post_create(sender, instance, created, **kwargs):
    """
    Triggered after a new user is created.
    If the user is newly created and inactive, an email with an activation link is sent.
    """
    pass
    if created and not instance.is_active:
        tg = PRTG()
        token = tg.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_url = reverse('activate_user', kwargs={'uidb64': uid, 'token': token})
        relative_activation_url = activation_url.replace('/auth', 'auth')
        full_url = f'{settings.BACKEND_URL}{relative_activation_url}'
        domain_url = settings.REDIRECT_LANDING
        print(full_url)
        text_content = render_to_string(
            "emails/activation_email.txt",
            context={'user': instance, 'activation_url': full_url, 'domain_url': domain_url},
        )
        html_content = render_to_string(
            "emails/activation_email.html",
            context={'user': instance, 'activation_url': full_url, 'domain_url': domain_url},
        )
        subject = 'Confirm your email'
        connection = get_connection()
        connection.open()
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        
        connection.close()