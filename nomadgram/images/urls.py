
from . import views 
from django.urls import include, path

app_name = "images"
urlpatterns = [
    path("all/", view =views.ListAllImages.as_view(), name="all_images"),
    path("comments/", view =views.ListAllComments.as_view(), name="all_comments"),
    path("likes/", view =views.ListAllLikes.as_view(), name="all_likes"),
]