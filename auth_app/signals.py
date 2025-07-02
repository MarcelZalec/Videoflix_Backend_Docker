from auth_app.models import CustomUserModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import sendMail
from django_rq import get_queue


@receiver(post_save, sender=CustomUserModel)
def user_post_create(sender, instance, created, **kwargs):
    """
    Triggered after a new user is created.
    If the user is newly created and inactive, an email with an activation link is sent.
    """
    if created and not instance.is_active:
        queue = get_queue('default', autocommit=True)
        queue.enqueue(sendMail, instance)