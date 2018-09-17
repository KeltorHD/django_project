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

import sqlite3
import re

def index(request):
    return render(
        request,
        'index.html',
        {"people":len(User.objects.all())})

def faq(request):
    return render(
        request,
        'app/faq.html')


def update(request):
    pass
    # conn = sqlite3.connect("list.sqlite")
    # cursor = conn.cursor()

    # rows = cursor.execute("SELECT * FROM people")
    # people = []
    # classec = []
    # cls = ''
    # for row in rows:
    #     if row[1] == 'Ф. И. О.':
    #         a = row[0].splitlines()[0]
    #         classec.append(a)
    #         cls = a
    #         continue

    #     a = []
    #     for i in range(len(row)):
    #         a.append(row[i])
    #         a[0] = cls
    #     people.append(a)
    # for i in classec:
    #     record = SchoolClass(school_class=i, number=re.sub(r"\D", "", i))
    #     record.save()
    # for i in people:
    #     cls = SchoolClass.objects.filter(school_class='{}'.format(i[0]))
    #     if not i[1]:
    #         continue
    #     first_name = i[1].split(' ')[1]
    #     if not first_name:
    #         first_name = i[1].split('  ')[1]
    #     last_name = i[1].split(' ')[0]
    #     if not first_name:
    #         last_name = i[1].split('  ')[1]
    #     record = People(first_name=first_name,
    #         last_name=last_name,
    #         school_class=cls[0])
    #     record.save()
    # return '<h1>{}</h1>'.format(len(people))

@login_required
def class_detail_view(request, pk):
    state = State.objects.filter(school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
    cls = SchoolClass.objects.filter(id=pk)
    people = People.objects.filter(school_class=pk)
    stats = SchoolClass.objects.get(id=pk)
    stats.stats += 1
    stats.save()

    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + ' ' + last_name
    access = request.user.groups.get().name
    return render(
        request,
        'app/state_list.html',
        context = {'state': state, 'cls':cls, 'people':people, 'pk':pk, 'stats':stats.stats, 'access':access, 'name':name})


def class_list(request):
    cls = SchoolClass.objects.all()
    view_class = []
    number = [1,2,3,4,5,6,7,8,9,10,11]
    for i in number:
        a = []
        for d in cls:
            if i == d.number:
                a.append(d)
        view_class.append(a)
    return render(
        request,
        'app/schoolclass_list.html',
        {'view_class':view_class})

@login_required
def writeindex(request):
    if request.user.groups.get().name == 'Writer':
        cls = SchoolClass.objects.all()
        view_class = []
        number = [1,2,3,4,5,6,7,8,9,10,11]
        for i in number:
            a = []
            for d in cls:
                if i == d.number:
                    a.append(d)
            view_class.append(a)
        state_list = State.objects.filter(availability='+').order_by('-date')[0:5]
        return render(
            request,
            'app/writeindex.html',
            context = {'view_class':view_class, 'state_list':state_list})
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
        d = []
        cls =  State.objects.filter(id=pk)
        clas = cls.values('school_class')
        people1 = People.objects.filter(school_class__school_class=clas[0]['school_class']).values_list('id')
        people = []
        for i in range(len(people1)):
            people.append(people1[i][0])
        select = []
        for i in form['people']:
            if i.data['value'] in people:
                select.append(i)
        return render(request, 
            'app/edit.html', 
            {'form': form,'id':pk, 'people':select, 'date':state.date})
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
            if User.objects.filter(email=email).exists():
                error = 'Пользователь с такой почтой уже зарегистрирован!'
                return render(
                    request,
                    'app/register.html',
                    {'error':error})
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
    state_list = State.objects.all().count()
    state_your = State.objects.filter(author=request.user).count()
    return render(
        request,
        'app/account.html',
        {'first_name':first_name, 'last_name':last_name, 'email':email.lower(), 'access':access, 'state_list':state_list, 'state_your':state_your})

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
