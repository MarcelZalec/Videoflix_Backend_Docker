import os
import shutil
from videoflix_app.models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from videoflix_app.tasks import *
from django_rq import job, get_queue
from django.db import transaction

import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Processes the video after it has been created.
    Runs inside a database transaction to ensure consistency.
    """
    if created:
        queue = get_queue('default', autocommit=True)
        queue.enqueue(process_video, instance)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes all resolution-specific directories associated with the video file
    when the corresponding Video object is deleted from the database.
    """
    folder_path = os.path.dirname(instance.video_file.path)
    clear_folder_path = os.path.splitext(instance.video_file.path)[0]
    thumbnail = instance.thumbnail
    if os.path.exists(folder_path):
        resolution = ['240p', '360p', '480p', '720p', '1080p']
        for res in resolution:
            file_path = os.path.join(folder_path, f"{os.path.basename(clear_folder_path)}_{res}_hls")
            if os.path.isdir(file_path):
                try:
                    shutil.rmtree(file_path)
                except Exception as e:
                    logger.error(f"Error removing file {file_path}: {e}")

    if thumbnail and hasattr(thumbnail, 'path'):
        try:
            os.remove(thumbnail.path)
        except FileNotFoundError:
            pass