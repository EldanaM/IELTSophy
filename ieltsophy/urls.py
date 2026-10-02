"""
URL configuration for ieltsophy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from .views_pages import index, ProtectedView
from reading.views import get_text, check_answers, get_videos, get_profile, get_history, vocabulary, delete_word, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('register/', register, name='register'),
    path('', index, name='index'),

    path('tests/', ProtectedView.as_view(template_name='tests.html'), name='tests'),
    path('text/', ProtectedView.as_view(template_name='text.html'), name='text'),
    path('result/', ProtectedView.as_view(template_name='result.html'), name='result'),
    path('profile/', ProtectedView.as_view(template_name='profile.html'), name='profile'),
    path('vocabulary/', ProtectedView.as_view(template_name='vocabulary.html'), name='vocabulary'),

    path('api/text/', get_text, name='get_text'),
    path('api/check/', check_answers, name='check_answers'),
    path('api/videos/', get_videos, name='get_videos'),
    path('api/profile/', get_profile, name='get_profile'),
    path('api/history/', get_history, name='get_history'),
    path('api/vocabulary/', vocabulary, name='vocabulary_api'),
    path('api/vocabulary/<int:word_id>/', delete_word, name='delete_word'),
]