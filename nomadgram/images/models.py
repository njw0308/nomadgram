from django.db import models
from nomadgram.users import models as user_models #닉네임으로 사용. 장고가 제공해주는 models 와 같으면 안되니까!
from taggit.managers import TaggableManager

class TimeStampModel(models.Model):
    #DatetimeField
    #https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.DateField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta: # 데이터베이스에는 존재하지 않지만 다른 모델들을 위한 base 가 되어주는 놈. abstract = True
        abstract = True

#relationship 모델!! one to many / many to many / --> 실세계에 맞게 우리가 구성하면 됨
class Image(TimeStampModel):
    file = models.ImageField()
    location = models.CharField(max_length = 140)
    caption = models.TextField()
    #[LOOK IN ALL THE COMMENTS FOR THE ONES THAT HAVE 'image'= THIS IMAGE ID] '_set' 메소드?  --> "숨겨진 필드(hidden field)"
    creator = models.ForeignKey(user_models.User, on_delete = models.PROTECT, related_name = 'images', null=True )
    tags = TaggableManager()
    
    #property? https://stackoverflow.com/questions/33379587/django-whats-the-difference-between-a-model-field-and-a-model-attribute/33379814#33379814
    #          https://dojang.io/mod/page/view.php?id=2476
    # --> 이것을 통해서 모델에 추가적으로 부가된 속성. --> 'field' 처럼 사용이 가능함.  ex) image.count_likes 이렇게
    @property
    def like_count(self):
        # 장고가 지원해주는 aggregate func  ' count () ' --> https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#cheat-sheet
        return self.likes.all().count() 
    
    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self): #메타클래스- "string represntation". imageobject 이렇게 보이는게 아니고, 바로 내가 지정한데로 보이도록.
        #https://docs.djangoproject.com/en/1.11/ref/models/instances/#other-model-instance-methods
        return '{} - {} ' .format(self.location, self.caption)

    #ordering? https://docs.djangoproject.com/en/2.2/ref/models/options/#django.db.models.Options.ordering
    class Meta:
        ordering = ['-created_at']

class Comment(TimeStampModel): 
    message = models.TextField()
    creator = models.ForeignKey(user_models.User , on_delete = models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete = models.CASCADE, related_name = 'comments', null= True)

    def __str__(self):
        return self.message

class Like(TimeStampModel):
    creator = models.ForeignKey(user_models.User, on_delete = models.PROTECT, null=True)
    # related_name? - foreignkey 에서 사용되는 놈. 
    # -> https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django/2642645#2642645
    # or https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ForeignKey.related_name
    image = models.ForeignKey(Image ,on_delete = models.CASCADE, related_name='likes', null=True)

    def __str__(self):
        return ' User : {}- Image Caption: {}'.format(self.creator.username, self.image.caption)