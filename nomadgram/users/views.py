from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #https://www.django-rest-framework.org/api-guide/status-codes/
from . import models, serializers

class ExploreUser(APIView):
    def get(self ,request ,format=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5] 
        # -> AbstractUser 에서 data_joined 필드가 있음. /최근에 가입한 순서대로!
        serializer = serializers.ExploreUserSerializer(last_five, many = True)

        return Response(data = serializer.data , status = status.HTTP_200_OK)
        