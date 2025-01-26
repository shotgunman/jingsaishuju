"""
URL configuration for jingsaishuju project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dataread import views
from dataread.views import RegisterView, LoginView, UserDetailView, Project_Create, Project_Del, Project_Get, \
    GetAllCompetitions
from rest_framework.views import APIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('create_project/', Project_Create.as_view(), name='create_project'),
    path('get_competitions_by_field/', Project_Get.as_view(), name='get_competitions_by_field'),
    path('get_all_competitions/', GetAllCompetitions.as_view(), name='get_all_competitions'),
    path('delete_competition/',Project_Del.as_view(), name='delete_competition'),
]
