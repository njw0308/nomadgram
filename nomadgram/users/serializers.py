from rest_framework import serializers
from . import models
from nomadgram.images import serializers as images_serializers


class UserProfileSerializer(serializers.ModelSerializer):

    images = images_serializers.CountImageSerializer(many = True, read_only = True)
    # read_only? I'd use read_only when is a field that I will never ever ever update.
    """
    I'd use read_only when is a field that I will never ever ever update. 
    Required I will use when I will maybe update it but I don't have to do it with every request.
    For example the profile fields, many of them are optional 
    when I'm updating because sometimes I want to update the name only and not update the email, so I will leave it required=false. 
    What would be read only would be for example the 'file' field of and image 
    since I want to make sure that I will never modify it.
    """
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