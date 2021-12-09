"""quiz_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from quizez import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizez.urls', namespace="quizez")),
    path('', views.home, name='home'),

    # leaderboard and result
    path('leaderboard/', views.leaderboards, name='leaderboards'),
    path('results/', views.results, name='results'),



    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # addquiz

    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_options/<int:myid>/', views.add_options, name='add_options'),
    path('delete_question/<int:myid>/',
         views.delete_question, name='delete_question'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
