from django.db import models
from nomadgram.users import models as user_models #닉네임으로 사용. 장고가 제공해주는 models 와 같으면 안되니까!

class TimeStampModel(models.Model):
    #DatetimeField
    #https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.DateField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta: # 데이터베이스에는 존재하지 않지만 다른 모델들을 위한 base 가 되어주는 놈.
        abstract = True

#relationship 모델!! one to many / many to many / --> 실세계에 맞게 우리가 구성하면 됨
class Image(TimeStampModel):
    file = models.ImageField()
    location = models.CharField(max_length = 140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete = models.PROTECT,null=True )
    #[LOOK IN ALL THE COMMENTS FOR THE ONES THAT HAVE 'image'= THIS IMAGE ID]
    def __str__(self): #메타클래스- "string represntation". imageobject 이렇게 보이는게 아니고, 바로 내가 지정한데로 보이도록.
        return '{} - {} ' .format(self.location, self.caption)

class Comment(TimeStampModel): 
    message = models.TextField()
    create = models.ForeignKey(user_models.User , on_delete = models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete = models.CASCADE, null= True)

    def __str__(self):
        return self.message

class Like(TimeStampModel):
    creator = models.ForeignKey(user_models.User, on_delete = models.PROTECT, null=True)
    image = models.ForeignKey(Image ,on_delete = models.CASCADE, null=True)

    def __str__(self):
        return ' User : {}- Image Caption: {}'.format(self.creator.username, self.image.caption)