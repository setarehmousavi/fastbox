from django.urls import path
from user.views import index_view

app_name = "user"

urlpatterns = [
    path('',index_view,name='index'),
  
]
