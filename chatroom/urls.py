from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatView, name='home'),
    path('about/<int:pk>/', views.ChatDetailView.as_view(), name='about_room'),
    path('chatroom/<int:pk>/', views.chatRoom, name='chatroom'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete_message'),

    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update_room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete_room'),
]
