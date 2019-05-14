from rest_framework import serializers
from . import models
from nomadgram.users import serializers as user_serializers
from nomadgram.images import serializers as image_seralizers
class NotificationSerializer(serializers.ModelSerializer):

    creator = user_serializers.ListUserSerializer()
    image = image_seralizers.SmallIamgeSerializer()
    class Meta:
        model = models.Notification
        fields = '__all__'