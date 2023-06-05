from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('sign-up/', views.signupUser, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/<int:pk>', views.userProfile, name='user-profile')
]
