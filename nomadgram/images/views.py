from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #https://www.django-rest-framework.org/api-guide/status-codes/
from . import models, serializers
from nomadgram.notification import views as notification_views
from nomadgram.users import models as user_models
from nomadgram.users import serializers as user_serializers

class Images(APIView):
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
        
        #내가 포스팅한 이미지도 보여줘야 하니까. 
        my_images = user.images.all()[:2]
        for image in my_images:
            if image not in image_list: # 중복되면 보기 싫으니까 추가해주자.
                image_list.append(image)
        
        #sorted? https://www.pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
        image_list = sorted(image_list, key=lambda image: image.created_at ,reverse= True) # 이미지 리스트를 다시 한 번 최신순으로 정렬
        serializer = serializers.ImageSerializer(image_list, many =True)
        return Response(data = serializer.data)

    #Uploading phote
    def post(self , request,  format = None):
        user = request.user
        serializer = serializers.InputImageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(creator =user)
            return Response(data = serializer.data , status = status.HTTP_201_CREATED)
        else:
            return Response(data = serializer.errors , status = status.HTTP_400_BAD_REQUEST)


class LikeImage(APIView):

    def get(self , request,  image_id , format =None):
        likes = models.Like.objects.filter(image__id = image_id)
        like_creator_ids = likes.values('creator_id')
        # -> https://docs.djangoproject.com/ko/2.1/ref/models/querysets/#django.db.models.query.QuerySet.values

        users = user_models.User.objects.filter(id__in = like_creator_ids) 
        # -> 누가 이 이미지를 '좋아요' 했는지가 궁금해!
        serializer = user_serializers.ListUserSerializer(users, many =True)
        return Response( data = serializer.data , status = status.HTTP_200_OK)
    #image_id 가 논항으로 들어올 수 있는 이유는 url 에서 그렇게 보내기 때문.
    def post(self, request , image_id,  format = None):
    
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist: #https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.DoesNotExist
            return Response(status = status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like= models.Like.objects.get(
                creator = request.user,
                image = found_image
            )
            return Response(status= status.HTTP_304_NOT_MODIFIED) 
        
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
            creator= request.user,
            image = found_image
            )

            #notification for Like
            notification_views.create_notification(
                request.user , found_image.creator, 'like', found_image)
            new_like.save()
            return Response(status= status.HTTP_201_CREATED)

#Like 와 UnLike 로 url 을 구분해서 따로 view 를 생성해준다.
class UnLikeImage(APIView):
    
    def delete(self, request , image_id , format=None):
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
            return Response(status= status.HTTP_304_NOT_MODIFIED) 


class CommentOnImage(APIView):
    
    def post(self, request,image_id , format=None): #get 이 아니라 post. --> DB에 무언가를 생성.

        user = request.user
        serializer= serializers.CommentSerializer(data = request.data) #시리얼라이저를 통해 디비에 데이터를 추가하려함.
        # commentserial 의 모델을 바탕(Meta 클래스에서 지정한데로) 으로 해서 만들어진데~
        # request.data? https://www.django-rest-framework.org/api-guide/requests/#data
        # --> dict 형 , ex) {"message":"test"}
        try:
            found_image= models.Image.objects.get(id= image_id)
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        if serializer.is_valid(): # https://www.django-rest-framework.org/api-guide/serializers/#validation
            serializer.save(creator= user, image = found_image)#https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
            # --> serializer 에 image 필드가 없는데도 가능한가봐!!(원래 모델에는 있어서!?)
            # --> For turning the JSON object that comes to the API into a python object!!
            # 참조!! https://www.django-rest-framework.org/api-guide/serializers/#serializing-objects
            #        https://www.django-rest-framework.org/api-guide/serializers/#deserializing-objects
            
            #notification for Comment
            notification_views.create_notification(
                user , found_image.creator, 'comment', found_image, serializer.data['message'])
            return Response(data =serializer.data ,status = status.HTTP_201_CREATED)

        else:
            return Response(data =serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Comment(APIView):
    
    def delete(self, request , comment_id, format=None):
        
        user = request.user
        print(user)
        try:
            comment = models.Comment.objects.get(id = comment_id, creator= user) 
            # id --> url 을 통해 들어올 것임. / creator --> 삭제를 요청하는 user 와 같아야 삭제가 가능하도록.(남이 나의 댓글을 삭제할 순 없잖아?)
            comment.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
class Search(APIView):

    def get(self, request , format=  None):
        
        hashtags = request.query_params.get('hashtags',None) # https://www.django-rest-framework.org/api-guide/requests/#query_params
        if hashtags is not None:
            hashtags= hashtags.split(',')
            images = models.Image.objects.filter(tags__name__in = hashtags).distinct() 
            # --> https://docs.djangoproject.com/ko/2.1/ref/models/querysets/#in
            # --> https://django-taggit.readthedocs.io/en/latest/api.html#filtering
            # addition. https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups
            serializer = serializers.CountImageSerializer(images, many =True)
            return Response(data =serializer.data, status = status.HTTP_200_OK)
        
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

#이상한 댓글 적혀있으면 그 이미지의 주인이 지우고 싶어!! 그 기능을 구현해보자.
class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format = None):
        user = request.user
        """
        try:
            image = models.Image.objects.get(id =image_id , creator = user)
        except models.Image.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        """
        try:
            #comment 안에 foreinKey 로 image 가 있기 때문에.
            comment_to_delete = models.Comment.objects.get(
                id= comment_id, image__id = image_id , image__creator = user)
            comment_to_delete.delete()
        except models.Image.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        
        return Response(status = status.HTTP_204_NO_CONTENT)

class ImageDetail(APIView):
    
    
    def find_own_image(self, image_id , user):
         try:
            image = models.Image.objects.get(id = image_id, creator = user) # creator 로 판별하는거 중요!!
            return image
         except models.Image.DoesNotExist:
            return None

    def get(self, request , image_id , format = None):
        user = request.user
        try: 
            image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = serializers.ImageSerializer(image)
        return Response(data =serializer.data, status = status.HTTP_200_OK)
    
    #내가 생성한 이미지를 편집하고 싶을 때.
    def put(self, request , image_id , format = None):
        """
        # 반복되니까 다른 함수로 만들어주자!!
        user = request.user
        try:
            image = models.Image.objects.get(id = image_id, creator = user)
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        """    
        image = self.find_own_image(image_id , user)
        if image is None:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.InputImageSerializer(image, data = request.data, partial =True)
        # -> https://www.django-rest-framework.org/api-guide/serializers/#partial-updates
        # -> InputImageSerializer 의 3가지 필드를 모두 작성하지 않아도 괜찮다!
        if serializer.is_valid():
            serializer.save(creator = user)   
            return Response(data = serializer.data , status= status.HTTP_204_NO_CONTENT)
        else:
            return Response(data = serializer.data , status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request , image_id , format =None):
        user = request.user
        image = self.find_own_image(image_id , user)
        if image is None:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        image.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)