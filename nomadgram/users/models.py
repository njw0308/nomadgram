from django.contrib.auth.models import AbstractUser

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

#Model documentation 을 보면 도움될거임.
#https://docs.djangoproject.com/en/1.11/topics/db/models/
class User(AbstractUser):

    GENDER_CHOICES= (
        ('male','Male'),
        ('female', 'Female'),
        ('not-specified' ,'Not-specified')
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(null= True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    website = models.URLField(null =True)
    bio = models.TextField(null =True)
    phone = models.CharField(max_length =140,null =True)
    gender = models.CharField(max_length=80, choices = GENDER_CHOICES,null =True)
    followers = models.ManyToManyField("self", blank= True) # relation 데이터베이스 구현을 이렇게 하자! 자기 자신 --> "self"
    # 팔로워나 팔로잉이 없어도 계정 생성은 되야하니까.
    following = models.ManyToManyField("self", blank =True)

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def followings_count(self):
        return self.following.all().count()