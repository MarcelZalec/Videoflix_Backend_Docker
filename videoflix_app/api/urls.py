from django.urls import path, include
from videoflix_app.api.views import VideoView, SingleVideoView

urlpatterns = [
    path('videos/', VideoView.as_view(), name='videos'),
    path('video/<int:video_id>/', SingleVideoView.as_view(), name='video-detail'),
]