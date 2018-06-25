from django.shortcuts import render, redirect, get_object_or_404
from .models import People, State, SchoolClass
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import StateForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group

def index(request):

    group = request.user.groups.get().name
    print(group)
    return render(
        request,
        'index.html')

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
    if request.user.groups.get().name == 'Writer':
        school_class = SchoolClass.objects.all()
        state_list = State.objects.order_by('-date')[0:5]
        return render(
            request,
            'app/writeindex.html',
            context = {'class':school_class, 'state_list':state_list})
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def newwrite(request, pk):
    if request.user.groups.get().name == 'Writer':
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
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def edit(request, pk, kl):
    if request.user.groups.get().name == 'Writer':
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
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def list(request):
    if request.user.groups.get().name == 'Writer':
        state = State.objects.order_by('-date')[0:50]
        return render(
            request,
            'app/list.html',
            context = {'state':state})
    else:
        return render(
            request,
            'app/permissions.html')


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
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(
        request,
        'app/login.html',
        {'form': form})
def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            if User.objects.filter(username=username) != None:
                messages.error(request, 'Пользователь с таким логином уже существует')
            email = form.cleaned_data.get('email', None)
            first_name = form.cleaned_data.get('first_name', None)
            last_name = form.cleaned_data.get('last_name', None)
            password1 = form.cleaned_data.get('password1', None)
            password2 = form.cleaned_data.get('password2', None)
            if password2 != password1:
                messages.error(request, 'Пароли не совпадают')
            user = User.objects.create_user(username, email, password1)
            user.first_name=first_name
            user.last_name=last_name
            group = Group.objects.get(name='Member')
            user.groups.add(group)
            user.save()
            log = authenticate(username=username, password=password1)
            auth.login(request, log)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(
        request,
        'app/register.html',
        {'form':form})
