from rest_framework import serializers
from . import models

#model 에서 정의한 field 를 사용하기 위해서는 ModelSerializer 를 사용한다.

class CommentSerializer(serializers.ModelSerializer):
    #image = ImageSerializer()
    class Meta:
        model = models.Comment
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    #image = ImageSerializer() # image 의 Foriegn key 만 갖고 오는 것이 아니라 , image 필드에서는 
                              # 이미 만들어놓은 imageserializer 를 통해 다 갖고 오도록 하는. 
    class Meta:
        model = models.Like
        fields = "__all__"
    
class ImageSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many =True)
    
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comment_set',
            'like_set',
        )
