from rest_framework import serializers
from . import models
from nomadgram.users import models as user_models 

#model 에서 정의한 field 를 사용하기 위해서는 ModelSerializer 를 사용한다.

class FeedUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image',
        )

class CommentSerializer(serializers.ModelSerializer):
    #image = ImageSerializer()
    creator = FeedUserSerializer(read_only=True) #https://www.django-rest-framework.org/api-guide/fields/#read_only
    # --> we make it read only because we want to pass the creator from the request.user. and not from the serializer.
    class Meta: #메타 클래스 --> extra 정보.
        #https://www.django-rest-framework.org/api-guide/serializers/#specifying-which-fields-to-include
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )

class LikeSerializer(serializers.ModelSerializer):
    #image = ImageSerializer() # image 의 Foriegn key 만 갖고 오는 것이 아니라 , image 필드에서는 
                              # 이미 만들어놓은 imageserializer 를 통해 다 갖고 오도록 하는. 
    class Meta:
        model = models.Like
        fields = "__all__"



class ImageSerializer(serializers.ModelSerializer):
    #nested 시리얼라이저 : https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    # --> Meta 클래스에서 지정된 모델, 그 모델에 해당하는 필드(attribute)를 가져올꺼임.
    # --> ' _set'과 같은 field 는 one to many relationship에서 장고 자체가 지원해주는 얘.
    # --> ex) 하나의 이미지에 여러 개의 comment 와 여러 개의 likes 가 달려 있을테니까.    
    # --> 어쨌든 그 중에 comment_set field 를 일반 상태(- foreign key 만)가 아닌 nested 를 한 얘 전체를 다 보여주는 것. 
    # --> comment_set -> comments 어떻게? models 에서 'related_name' 논항을 통해 변환. 
    # --> default 는 comment_set 이지만 이제는 '내가 지정한 이름' 으로 그 필드를 사용하겠다!
    
    comments= CommentSerializer(many =True)
    #likes = LikeSerializer(many = True)
    creator = FeedUserSerializer() #creator 는 한 명이니까 many =True 하면 안되겠지!

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
        )
