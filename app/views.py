from django.shortcuts import render, redirect, get_object_or_404
from .models import People, State, SchoolClass
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import StateForm, LoginForm
from django.contrib.auth import authenticate
from django import forms
from django.contrib import messages
from django.contrib import auth

def index(request):
    num_state = State.objects.all().count()
    num_people = People.objects.all().count()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context = {'num_date':num_state, 'num_people':num_people, 'num_visits':num_visits})

def faq(request):
    return render(
        request,
        'app/faq.html')

def class_detail_view(request, pk):
    state = State.objects.filter(school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()))
    stistic = SchoolClass.objects.filter(id='{}'.format(pk))
    people = People.objects.filter(school_class='{}'.format(pk))
    return render(
        request,
        'app/state_list.html',
        context = {'state': state, 'cls':stistic, 'people':people})


class ClassListView(generic.ListView):
    model = SchoolClass

@login_required
def writeindex(request):
    school_class = SchoolClass.objects.all()
    state_list = State.objects.order_by('-date')[0:5]
    return render(
        request,
        'app/writeindex.html',
        context = {'class':school_class, 'state_list':state_list})

@login_required
def newwrite(request, pk):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.status = '+'
            state.school_class = SchoolClass.objects.filter(id = '{}'.format(pk)).first()
            state.school_class_id = str(pk)
            state.save()
            form.save_m2m()
            return redirect('writeindex')
    else:
        form = StateForm()
        form.fields['people'].queryset = People.objects.filter(school_class='{}'.format(pk))
    return render(
        request,
        'app/newwrite.html',
        context = {'form':form})

@login_required
def edit(request, pk, kl):
    state = get_object_or_404(State, pk=pk)
    if request.method == "POST":
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            state = form.save(commit=False)
            state.status = '+'
            state.save()
            form.save_m2m()
            return redirect('writeindex')
    else:
        form = StateForm(instance=state)
    return render(request, 
        'app/newwrite.html', 
        {'form': form})

@login_required
def list(request):
    state = State.objects.order_by('-date')[0:50]
    return render(
        request,
        'app/list.html',
        context = {'state':state})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("Логин или пароль неверны")
                messages.error(request, 'Неверны логин или пароль')
    else:
        form = LoginForm()
    return render(
        request,
        'app/login.html',
        {'form': form})
#from django.contrib.auth.decorators import login_required

#@login_required
#def abc(request) - для проверки на регистрацию