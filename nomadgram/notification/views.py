from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
# Create your views here.

class Notifications(APIView):

    def get(self, request , format =None):
        user= request.user
        notifications = models.Notification.objects.filter(to = user)
        serializer= serializers.NotificationSerializer(notifications , many= True)
        return Response(data = serializer.data , status = status.HTTP_200_OK)


def create_notification(creator, to , notification_type, image = None , comment = None):

    notification = models.Notification.objects.create(
        creator = creator,
        to = to,
        notification_type = notification_type,
        image =image,
        comment = comment,
    )
    notification.save()

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter