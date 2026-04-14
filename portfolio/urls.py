from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Use custom logout
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze_portfolio, name='analyze_portfolio'),
    path('recommendations/', views.investment_recommendations, name='recommendations'),
]