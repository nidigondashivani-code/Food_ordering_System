from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('owner-register/', views.owner_register, name='owner_register'),
    path('own-register/', views.owner_register, name='own_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('delete/', views.delete_account, name='delete_account'),
]
