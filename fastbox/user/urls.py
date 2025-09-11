from django.urls import path
from user.views import index_view,RegisterView,LoginView,LogoutView

app_name = "user"

urlpatterns = [
    path('',index_view,name='index'),
    path('register/',RegisterView.as_view(),name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),name='logout') , 
]
