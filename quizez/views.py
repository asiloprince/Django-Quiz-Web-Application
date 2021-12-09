from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import *
from results.models import *
from .forms import QuizForm, QuestionForm
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'quizez/home.html')


def signupuser(request):

    if request.method == 'GET':
        return render(request, 'quizez/signupuser.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/main')
            except IntegrityError:
                return render(request, 'quizez/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'quizez/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'quizez/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'quizez/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('/main')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


class QuizListView(ListView):
    Model = Quiz
    template_name = 'quizez/main.html'
    context_object_name = "quiz"

    def get_queryset(self):
        return Quiz.objects.all()


@login_required
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizez/quiz.html', {'obj': quiz})


@login_required
def quiz_data_view(request, pk):

    quiz = Quiz.objects.get(pk=pk)
    question = []

    for q in quiz.get_questions():
        answer = []
        for a in q.get_answers():
            answer.append(a.text)
        question.append({str(q): answer})
    return JsonResponse({
        'data': question,
        'time': quiz.time,
    })


@login_required
def save_quiz_view(request, pk):
    print(request.POST)

    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print("keys ", k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                print(a_selected)
                questions_answers = Answer.objects.filter(question=q)

                for a in questions_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

            else:
                results.append({str(q): 'not answered'})
        final_res = score * multiplier
        print(final_res)
        Result.objects.create(quiz=quiz, user=user, score=final_res)

        return JsonResponse({'passed': True, 'score': final_res, 'results': results})


@login_required
def leaderboards(request):
    ranking_score = Result.objects.order_by('-score')
    total_count = ranking_score.count()
    context = {
        'ranking_score': ranking_score,
        'total_count': total_count,
    }
    return render(request, "quizez/leaderboard.html", context=context)


@login_required
def results(request):
    results = Result.objects.all()
    return render(request, "quizez/results.html", {'results': results})


# admin only if superuser
@login_required
def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            objs = form.instance
            return render(request, 'quizez/add_question.html', {'obj': objs})
    else:
        form = QuizForm()
    return render(request, 'quizez/addquiz.html', {'form': form})


@login_required
def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "quizez/add_question.html")
    else:
        form = QuestionForm()
    return render(request, "quizez/add_question.html", {'form': form, 'questions': questions})


@login_required
def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "quizez/delete_question.html", {'question': question})


@login_required
def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(
        Question, Answer, fields=('text', 'correct', 'question'), extra=4)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "quizez/add_options.html", {'alert': alert})
    else:
        formset = QuestionFormSet(instance=question)
    return render(request, "quizez/add_options.html", {'formset': formset, 'question': question})
