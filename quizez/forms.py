from django import forms
from questions.models import Question
from .models import Quiz
from django.contrib import admin


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'topic', 'difficulty',
                  'number_of_questions', 'time', 'required_score_to_pass')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'quiz')
