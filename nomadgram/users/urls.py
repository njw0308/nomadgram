from . import views 
from django.urls import include, path

app_name = "users"
urlpatterns = [ 
    path("explore/", view =views.ExploreUser.as_view(), name = "explore_user"),
]