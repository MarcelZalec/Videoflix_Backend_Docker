import os
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from videoflix_app.models import Video
from rest_framework.permissions import AllowAny


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, format=None):
        """
        Retrieve all videos from cache or database.

        :param request: HTTP GET request
        :param format: Optional request format
        :return: JsonResponse with a list of video objects (HTTP 200)
        """
        cached_videos = cache.get('all_videos')
        if cached_videos is None:
            videos = Video.objects.all()
            cached_videos = list(videos.values())
            cache.set('all_videos', cached_videos, timeout= CACHE_TTL)
        return JsonResponse(cached_videos, safe=False)
        # serializer = VideoSerializer(videos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new video instance.

        :param request: HTTP POST request with video data
        :return: JSON response with created video data (HTTP 200) or error (HTTP 400)
        """
        serializer = VideoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleVideoView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, video_id):
        """
        Retrieve a single video by its ID.

        :param request: HTTP GET request
        :param video_id: ID of the video to retrieve
        :return: Serialized video data (HTTP 200) or 404 if not found
        """
        video = Video.objects.get(pk = video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, video_id):
        """
        Delete a video by its ID.

        :param request: HTTP DELETE request
        :param video_id: ID of the video to delete
        :return: Confirmation message (HTTP 200) or 404 if not found
        """
        video = Video.objects.get(pk = video_id)
        serializer = VideoSerializer(video)
        video.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, video_id):
        """
        Update an existing video instance.

        :param request: HTTP PUT request with partial or full video data
        :param video_id: ID of the video to update
        :return: Updated video data (HTTP 200) or validation errors (HTTP 400)
        """
        video = Video.objects.get(pk = video_id)
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)