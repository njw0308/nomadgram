from rest_framework import serializers
from . import models
from nomadgram.images import serializers as images_serializers


class UserProfileSerializer(serializers.ModelSerializer):

    images = images_serializers.CountImageSerializer(many = True)
    followers_count = serializers.ReadOnlyField() 
    # -> https://www.django-rest-framework.org/api-guide/fields/#readonlyfield
    # -> 해당 필드는 수정하지 않겠움!!
    followings_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'followings_count',
            'images',
        )

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
        )