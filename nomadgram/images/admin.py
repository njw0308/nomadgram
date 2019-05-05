from django.contrib import admin
from . import models

# Register your models here.
#데코레이터를 통해 모델에 있는 field name들이 admin 패널에서 보이더라.
@admin.register(models.Image) 
class ImageAdmin(admin.ModelAdmin):

    # admin 쪽에서 링크를 바로 탈 수 있게끔 하는 놈.
    list_display_links = (
        'location',
    )
    
    # admin 안에 검색 기능 추가.
    search_fields = (
        'location', 
        'caption',
    )

    # filter 기능. 
    list_filter = (
        'location',
        'creator',
    )
    
    # admin 사이트에서 볼 수 있도록. 안에
    #  모델에 있는 칼럼명.
    list_display = (
        'file',
        'location',
        'caption',
        'creator',
        'created_at',
        'updated_at',
    )
    pass

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        'creator',
        'image',
        'created_at',
        'updated_at',
    )
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    # admin 사이트에서 볼 수 있도록. 안에 모델에 있는 칼럼명.
    list_display = (
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )
    pass
