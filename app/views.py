from django.shortcuts import render, redirect, get_object_or_404
from .models import People, State, SchoolClass, User
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import StateForm, LoginForm, RegisterForm, PasrecForm
from django.contrib.auth import authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
import datetime

def index(request):
    return render(
        request,
        'index.html',
        {"people":len(User.objects.all())})

def faq(request):
    return render(
        request,
        'app/faq.html')
    
@login_required
def class_detail_view(request, pk):
    state = State.objects.filter(school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
    cls = SchoolClass.objects.filter(id='{}'.format(pk))
    people = People.objects.filter(school_class='{}'.format(pk))
    return render(
        request,
        'app/state_list.html',
        context = {'state': state, 'cls':cls, 'people':people, 'pk':pk})

@login_required
def class_detail_view_order(request,pk,kl):
    cls = SchoolClass.objects.filter(id='{}'.format(pk))
    people = People.objects.filter(school_class='{}'.format(pk))
    if kl == 'month':
        state = State.objects.filter(date__gt=datetime.date.today() + datetime.timedelta(days=-32), school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
        order = '1'
    elif kl == 'half_a_year':
        state = State.objects.filter(date__gt=datetime.date.today() + datetime.timedelta(days=-183), school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
        order = '2'
    else:
        state = State.objects.filter(school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
        order = '3'
    return render(
        request,
        'app/state_list.html',
        {'state': state, 'cls':cls, 'people':people, 'order':order})

def class_list(request):
    school_class = SchoolClass.objects.order_by('id')
    return render(
        request,
        'app/schoolclass_list.html',
        {'school_class':school_class})

@login_required
def writeindex(request):
    if request.user.groups.get().name == 'Writer':
        school_class = SchoolClass.objects.order_by('id')
        state_list = State.objects.filter(availability='+').order_by('-date')[0:5]
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
                state.availability = '+'
                state.author = str(request.user)
                state.save()
                form.save_m2m()
                return redirect('writeindex')
        else:
            form = StateForm()
            form.fields['people'].queryset = People.objects.filter(school_class='{}'.format(pk))
            people = People.objects.filter(school_class='{}'.format(pk))
        return render(
            request,
            'app/newwrite.html',
            context = {'form':form,'people':people})
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def edit(request, pk):
    if request.user.groups.get().name == 'Writer':
        state = get_object_or_404(State, pk=pk)
        if request.method == "POST":
            form = StateForm(request.POST, instance=state)
            if form.is_valid():
                state = form.save(commit=False)
                state.status = '+'
                state.author = str(request.user)
                state.save()
                form.save_m2m()
                return redirect('writeindex')
        else:
            form = StateForm(instance=state)
        return render(request, 
            'app/edit.html', 
            {'form': form,'id':pk})
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def delete(request,pk):
    if request.user.groups.get().name == 'Writer':
        state = get_object_or_404(State, pk=pk)
        if request.method == "POST":
            state.availability = '-'
            state.save()
            return redirect('writeindex')
        else:
            return render(
                request,
                'app/delete.html',
                {'state':state})
    else:
        return render(
            request,
            'app/permissions.html')

@login_required
def list(request):
    if request.user.groups.get().name == 'Writer':
        state = State.objects.filter(availability='+').order_by('-date')[0:50]
        return render(
            request,
            'app/list.html',
            context = {'state':state})
    else:
        return render(
            request,
            'app/permissions.html')

def confidencial(request):
    return render(
        request,
        'app/confidencial.html')


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
                    error = 'Ваш аккаунт выключен - напишите разработчику: keltorplaylife@gmail.com!'
                    return render(
                        request,
                        'app/login.html',
                        {'error':error})
            else:
                error = 'Неверный логин или пароль!'
                return render(
                    request,
                    'app/login.html',
                    {'error':error})
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
            kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
            username = form.cleaned_data.get('username', None)
            find_kirill = [x for x in kirill if x in username.lower()]
            if (len(username)<6) or (find_kirill):
                error = 'Логин меньше 6 символов или написан не латиницей!'
                return render(
                    request,
                    'app/register.html',
                    {'error':error})
            if User.objects.filter(username=username).exists():
                error = 'Пользователь с таким логином уже существует!'
                return render(
                    request,
                    'app/register.html',
                    {'error':error})
            email = form.cleaned_data.get('email', None)
            first_name = form.cleaned_data.get('first_name', None)
            last_name = form.cleaned_data.get('last_name', None)
            password1 = form.cleaned_data.get('password1', None)

            find_kirill = [x for x in kirill if x in password1.lower()]
            if (find_kirill) or len(password1)<6:
                error = 'Пароль меньше 6 символов или написан не латиницей!'
                return render(
                    request,
                    'app/register.html',
                    {'error':error})

            password2 = form.cleaned_data.get('password2', None)
            if password2 != password1:
                error = 'Пароли не совпадают!'
                return render(
                    request,
                    'app/register.html',
                    {'error':error})
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

@login_required
def account(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    access = request.user.groups.get().name
    return render(
        request,
        'app/account.html',
        {'first_name':first_name, 'last_name':last_name, 'email':email.lower(), 'access':access})

@login_required
def pasrec(request):
    if request.method == 'POST':
        form = PasrecForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if request.user.check_password(password):
                if password2 == password1:
                    user = User.objects.get(username=request.user.username)
                    user.set_password('{}'.format(password1))
                    user.save()
                    log = authenticate(username=request.user.username, password=password1)
                    auth.login(request, log)
                    return redirect('account')
                else:
                    error = 'Новые пароли не совпадают!'
                    return render(
                        request,
                        'app/pasrec.html',
                        {'error':error})
            else:
                error = 'Старый пароль неверен!'
                return render(
                    request,
                    'app/pasrec.html',
                    {'error':error})
            
    else:
        form = PasrecForm()
    return render(
        request,
        'app/pasrec.html',
        {'form':form})
