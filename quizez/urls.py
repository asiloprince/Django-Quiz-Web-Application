from django.urls import path

from .views import *

app_name = 'quizez'

urlpatterns = [

    # quiz
    path('main/', QuizListView.as_view(), name='main-view'),
    path('main/<pk>/', quiz_view, name='quiz-view'),
    path('main/<pk>/save/', save_quiz_view, name='save-view'),
    path('main/<pk>/data/', quiz_data_view, name='quiz-data-view'),


]
