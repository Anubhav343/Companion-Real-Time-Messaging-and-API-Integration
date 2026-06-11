from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name = "home"),
    path('room_page/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/<str:pk>/', views.updateUser, name="update-user"),

    path('createroom/', views.createRoom, name="create-room"),
    path('updateroom/<str:pk>/', views.updateroom, name="update-room"),
    path('deleteroom/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('deletemessage/<str:pk>/', views.deleteMessage , name="delete-message"),


    path('topics/', views.topicsPage , name="topics"),
    path('activity/', views.activityPage , name="activity"),


]