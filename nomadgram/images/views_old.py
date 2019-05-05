from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
# Create your views here.

#Api view -> https://www.django-rest-framework.org/api-guide/views
#https://www.django-rest-framework.org/tutorial/3-class-based-views/
class ListAllImages(APIView):

    #httprequest--> https://docs.djangoproject.com/en/1.11/ref/request-response/#httprequest-objects
    def get(self, request , format = None):
        all_images = models.Image.objects.all()
        
        #https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-multiple-objects
        serializer = serializers.ImageSerializer(all_images, many =True)

        return Response(data = serializer.data) 

class ListAllComments(APIView):
    def get(self, request , format = None):
        print(request.user.id) #이 웹사이트를 요청하고 있는 user 의 아이디.

        #보통 누가 모델을 생성했는지를 기준으로 쿼리를 만든다!!
        #user_id = request.user.id
        #all_comments = models.Comment.objects.filter(creator = user_id )
        all_comments = models.Comment.objects.all()
        
        serializer = serializers.CommentSerializer(all_comments, many=True)
        return Response(data = serializer.data)
        
class ListAllLikes(APIView):
    def get(self, request , format=None):
        all_likes  = models.Like.objects.all()
        serializer = serializers.LikeSerializer(all_likes, many =True)
        return Response(data = serializer.data)