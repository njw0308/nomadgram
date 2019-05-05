from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #https://www.django-rest-framework.org/api-guide/status-codes/
from . import models, serializers

class Feed(APIView):
    def get(self, request, format=None):
        user =request.user
        following_users = user.following.all() #request 들어온 user가 following 하는 또 다른 user들의 목록.
        image_list = []
        for following_user in following_users:
             #following_user 에는 images 라는 필드가 없음
             #--> 이게 가능한 이유는 user 와 images 가 one -to -many 인데 related_name 을 통해서 '_set' 을 'images'로 이름을 바꿨기 때문.
            user_images =  following_user.images.all()[:2]  #가장 최근꺼 2개만. 
            for image in user_images:
                image_list.append(image) # 하나의 리스트로 다 같이 합쳐서 출력
            
        #sorted? https://www.pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
        image_list = sorted(image_list, key=lambda image: image.created_at ,reverse= True) # 이미지 리스트를 다시 한 번 최신순으로 정렬
        
        serializer = serializers.ImageSerializer(image_list, many =True)
        return Response(data = serializer.data)

class LikeImage(APIView):

    #image_id 가 논항으로 들어올 수 있는 이유는 url 에서 그렇게 보내기 때문.
    def get(self, request , image_id,  format = None):
    
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist: #https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.DoesNotExist
            return Response(status = status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like= models.Like.objects.get(
                creator = request.user,
                image = found_image
            )
            preexisting_like.delete()
            return Response(status= status.HTTP_204_NO_CONTENT) 
        
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
            creator= request.user,
            image = found_image
            )
            new_like.save()
            return Response(status= status.HTTP_201_CREATED)