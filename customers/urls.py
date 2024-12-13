from django.urls import path
from .views import register, customer_login, customer_logout,home,landing,get_users
urlpatterns = [
    path('',landing, name='landing'),
    path('home/',home, name='home'),
    path('register/', register, name='register'),
    path('login/', customer_login, name='customer_login'),
    path('logout/', customer_logout, name='customer_logout'),
    path('all/', get_users, name='get_users')
]