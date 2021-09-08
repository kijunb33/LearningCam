"""LearningCam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from log.views import IndexView, SummaryView, VideoView, AddLogView, VideoDetailView, VideoDetailModelView

app_name = 'log'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('summary', SummaryView.as_view(), name='summary'),
    path('video', VideoView.as_view(), name='video'),
    path('video/<int:pk>', VideoDetailView.as_view(), name='video-detail'),
    path('video/<int:pk>/model/<str:filename>', VideoDetailModelView.as_view(), name='video-detail-model'),
    path('log', AddLogView.as_view(), name='add'),
]

