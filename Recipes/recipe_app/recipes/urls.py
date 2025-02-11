from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Nova rota para editar perfil
    path('profile/<str:username>/', views.profile, name='profile'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:pk>/like/', views.like_recipe, name='like_recipe'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),
]