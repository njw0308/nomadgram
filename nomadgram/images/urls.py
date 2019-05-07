
from . import views 
from django.urls import include, path

app_name = "images"
urlpatterns = [
    ## the 'name' value as called by the {% url %} template tag
    path("" , view = views.Feed.as_view(), name = 'feed'),
    # url() -> path() : https://consideratecode.com/2018/05/02/django-2-0-url-to-path-cheatsheet/
    path("<int:image_id>/like/" , view = views.LikeImage.as_view() , name = 'like_image'),
    path("<int:image_id>/comment/" , view = views.CommentOnImage.as_view() , name = 'comment_image'),
    #path("all/", view =views.ListAllImages.as_view(),name="all_images"),
    #path("comments/", view =views.ListAllComments.as_view()), #name="all_comments"),
    #path("likes/", view =views.ListAllLikes.as_view()), #name="all_likes"),
]