from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Video
        fields = '__all__'


class SingleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Video
        fields = '__all__'
    
    def update(self, instance, validated_data):
        """
        Custom update method to manually assign new values to the instance fields.

        :param instance: The existing Video model instance to update
        :param validated_data: The validated data dictionary containing updated fields
        :return: The updated Video instance
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.video_file = validated_data.get('video_file', instance.video_file)
        instance.save()
        return instance