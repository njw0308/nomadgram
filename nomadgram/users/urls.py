from . import views 
from django.urls import include, path

app_name = "users"
urlpatterns = [ 
    path("explore/", view =views.ExploreUser.as_view(), name = "explore_user"),
    path("<int:user_id>/follow/", view = views.FollowUser.as_view(), name = "follow_user"),
    path("<int:user_id>/unfollow/", view = views.UnFollowUser.as_view(), name = "unfollow_user"),
    path("search/", view = views.Search.as_view(), name = "search"), #아래 url path 와 순서를 바꿔줘야함. 안그러면 search가 username인 줄 알오!!
    path("<str:username>/", view = views.UserProfile.as_view(), name = "user_profile"),
    path("<str:username>/followers/", view = views.UserFollowers.as_view(), name = "user_followers"),
    path("<str:username>/following/", view = views.UserFollowing.as_view(), name = "user_following"),
    
]