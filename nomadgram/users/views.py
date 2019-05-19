from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #https://www.django-rest-framework.org/api-guide/status-codes/
from . import models, serializers
from nomadgram.notification import views as notification_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class ExploreUser(APIView):
    def get(self ,request ,format=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5] 
        # -> AbstractUser 에서 data_joined 필드가 있음. /최근에 가입한 순서대로!
        serializer = serializers.ListUserSerializer(last_five, many = True)

        return Response(data = serializer.data , status = status.HTTP_200_OK)

class FollowUser(APIView):
    def post(self, request, user_id , format=None):
        user = request.user

        try:
            user_to_follow= models.User.objects.get(id = user_id)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        user.following.add(user_to_follow)
        user.save()

        # notification for follow
        notification_views.create_notification(user, user_to_follow, 'follow')
        return Response(status= status.HTTP_200_OK)

class UnFollowUser(APIView):
    def post(self, request, user_id , format=None):
        user = request.user
        try:
            user_to_follow= models.User.objects.get(id = user_id)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        user.following.remove(user_to_follow) 
        # --> delete() deletes an object from the database. .remove() deletes the many to many relationship between models.
        user.save()
        return Response(status= status.HTTP_200_OK)

class UserProfile(APIView):
    
    def get_user(self ,username):
        try:
            found_user = models.User.objects.get(username = username)
            
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request , username, format =None):
        
        found_user = self.get_user(username)    
        if found_user is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserProfileSerializer(found_user)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    
    #내 profile 을 수정하고 싶을 때.
    def put(self, request , username , formant= None):
        user = request.user
        found_user = self.get_user(username)    
        if found_user is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if found_user.username != user.username:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        
        serializer =serializers.UserProfileSerializer(
            found_user , data = request.data , partial = True)
        if serializer.is_valid(): # https://www.django-rest-framework.org/api-guide/serializers/#validation 
            serializer.save()
            return Response(data = serializer.data , status=  status.HTTP_200_OK)
        else:
            return Response(data = serializer.errors , status = status.HTTP_400_BAD_REQUEST)

class UserFollowers(APIView):

    def get(self , request, username, format =None):
        try:
            found_user = models.User.objects.get(username = username)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        user_followers = found_user.followers.all()
        serializer = serializers.ListUserSerializer(user_followers, many =True)
        
        return Response(data = serializer.data, status = status.HTTP_200_OK)

class UserFollowing(APIView):
    def get(self, request , username , format=None):
        try:
            found_user = models.User.objects.get(username = username)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        user_following = found_user.following.all()
        serializer = serializers.ListUserSerializer(user_following, many = True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)

class Search(APIView):
    
    def get(self, request, format=None):
        username = request.query_params.get('username',None)
        if username is not None:
            users = models.User.objects.filter(username__icontains = username)  #istartswith 도 가능.
            # --> https://docs.djangoproject.com/en/2.2/ref/models/querysets/#icontains
            serializer = serializers.ListUserSerializer(users, many =True)
            return Response(data = serializer.data, status = status.HTTP_200_OK)

        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):

    def put (self, request,username , format= None):
        user = request.user
        if user.username == username:
            current_pw = request.data.get('current_password',  None)
            # -> get? https://www.tutorialspoint.com/python/dictionary_get.htm
            if current_pw is not None:
                pw_match = user.check_password(current_pw) 
                # -> https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.check_password
                if pw_match:
                    new_pw = request.data.get('new_password',  None)
                    if new_pw is not None:
                        user.set_password(new_pw)
                        #-> https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.set_password
                        user.save()
                        return Response(status = status.HTTP_200_OK)
                    else:
                        return Response(status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter