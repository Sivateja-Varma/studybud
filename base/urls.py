from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.Login_user,name="login"),
    path('log-out/',views.Logut_user,name="logout"),
    path('register/',views.Register_user,name="register"),
    path('',views.home,name="home" ),
    path('profile/<str:pk>/',views.Profile,name="profile"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.Create,name='create'),
    path('update/<str:pk>/',views.Update,name="update"),
    path('delete/<str:pk>/',views.Delete,name="del"),
    path('deletemessage/<str:pk>/',views.DeleteMessage,name="deleted"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity")
]