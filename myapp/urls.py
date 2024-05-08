from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chat', views.chat, name="chat"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('deleteChat/<int:id>',views.deleteChat,name='deleteChat'),
    path('deleteAll/<int:id>',views.deleteAll,name='deleteAll'),
]