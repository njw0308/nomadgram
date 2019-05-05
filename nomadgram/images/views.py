from rest_framework.views import APIView
from rest_framework.response import Response
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