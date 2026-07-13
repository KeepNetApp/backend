from django.urls import path
from users.views import  get_me
urlpatterns = [
    path("me/", get_me)

]
