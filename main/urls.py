"""JustAsk URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.SignUp.as_view()),
    path('logout/', views.logout_handle),
    path('login/', views.Login.as_view()),
    path('AddQues/', views.add_question),
    path('MyQuestions/', views.MyQuestions),
    path('MyAnsweres/', views.MyAnsweres),
    path('answere/', views.answere_handle),
    path('search/', views.search),
    path('delete/<str:ques>/<int:id>/', views.delete),
    path('<str:ques>/<int:num>/', views.show_ques),

]
