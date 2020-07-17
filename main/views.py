from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from main.models import Question, Answere
from main.templatetags import extras
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
    allques = Question.objects.all().order_by('-date')
    ans = Answere.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(allques, 3)
    try:
        ques = paginator.page(page)
    except PageNotAnInteger:
        ques = paginator.page(1)
    except EmptyPage:
        ques = paginator.page(paginator.num_pages)
    return render(request, 'main/index.html', {'questions': ques, 'ans': ans})


def logout_handle(request):
    logout(request)
    messages.success(request, 'Logout successfully...')
    return redirect('/')


class SignUp(View):
    def post(self, request):
        name = request.POST.get('signupname')
        passwd = request.POST.get('signuppass')

        # check if username exists
        try:
            u = User.objects.get(username=name)
            messages.warning(request, 'Username already exists...')
            return redirect('/')
        except:
            if (len(name) > 2 and len(name) < 15) and (len(passwd) > 2 and len(passwd) < 15):
                usr = User.objects.create_user(name, None, passwd)
                login(request, usr,
                      backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Sign up successfully...')
            else:
                messages.error(
                    request, 'Username and password should be 3 to 15 characters...')
            return redirect('/')

    def get(self, request):
        return redirect('/')


class Login(View):
    def post(self, request):
        name = request.POST.get('loginname')
        passwd = request.POST.get('loginpass')
        usr = authenticate(username=name, password=passwd)
        if usr is not None:
            login(request, usr)
            messages.success(request, f'Welcome back {usr}')

        else:
            messages.error(request, 'Wrong Credientials...')
        return redirect('/')

    def get(self, request):
        return redirect('/')


def add_question(request):
    ques = request.GET.get('ques')
    qst = Question(ques=ques, user=request.user)
    qst.save()
    return redirect('/')


def show_ques(request, ques, num):
    # print('entered')
    # print(ques)
    question = Question.objects.get(ques=ques.replace('003qmark', '?'), pk=num)
    ans = Answere.objects.filter(ques=question)
    try:
        myans = Answere.objects.filter(
            user=request.user, ques=question)
    except:
        myans = Answere.objects.none()
    ans = myans | ans
    return render(request, 'main/ShowQues.html', {'ques': question, 'answeres': ans})


def MyQuestions(request):
    ques = Question.objects.filter(user=request.user).order_by('-date')
    if ques.count() == 0:
        messages.warning(request, 'You did not ask any answere yet...')
    return render(request, 'main/myques.html', {'questions': ques})


def answere_handle(request):
    if request.method == 'POST':
        ans = request.POST.get('ans')
        sno = request.POST.get('id')
        ques = request.POST.get('ques')
        qu = Question.objects.get(pk=sno)
        ans = Answere(ans=ans, user=request.user, ques=qu)
        ans.save()
        messages.success(request, 'Answere posted successfully...')
        print(ans)
        return redirect(f'/{ques}/{sno}')
    else:
        return redirect('/')


def MyAnsweres(request):
    ans = Answere.objects.filter(user=request.user)
    if ans.count() == 0:
        messages.warning(request, "You did not give any answere yet...")
    return render(request, 'main/myans.html', {'answeres': ans})


def search(request):
    search = request.GET.get('search')
    noresult = False
    s1 = Question.objects.filter(ques__icontains=search)
    if s1.count() == 0:
        s1 = Question.objects.all().order_by('-date')[:10]
        noresult = True
    return render(request, 'main/search.html', {'results': s1, 'noresult': noresult})


def delete(request, ques, id):
    if request.user.is_authenticated:
        ques = ques.replace('003qmark', '?')
        try:
            Question.objects.get(ques=ques, pk=id, user=request.user).delete()
        except:
            return redirect('/')
        return redirect('/MyQuestions')
    else:
        return redirect('/')
