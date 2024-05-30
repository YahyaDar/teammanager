from django.urls import path
from . import views


urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('faculty_user', views.register_user, name='register_user'),
    path('index', views.index, name='index'),
]
