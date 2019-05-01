from django.db import models
from nomadgram.users import models as user_models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True

class Image(TimeStampModel):
    file = models.ImageField()
    location = models.CharField(max_length = 140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete = models.PROTECT,null=True )
    #[LOOK IN ALL THE COMMENTS FOR THE ONES THAT HAVE 'image'= THIS IMAGE ID]
    def __str__(self): #메타클래스. imageobject 이렇게 보이는게 아니고, 바로 내가 지정한데로 보이도록.
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