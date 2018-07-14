from django.shortcuts import render, redirect, get_object_or_404
from .models import People, State, SchoolClass
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import StateForm, LoginForm, RegisterForm, PasrecForm
from django.contrib.auth import authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group

from PIL import Image
import PIL.Image

def index(request):
    return render(
        request,
        'index.html')

def faq(request):
    return render(
        request,
        'app/faq.html')
    
@login_required
def class_detail_view(request, pk):
    state = State.objects.filter(school_class='{}'.format(SchoolClass.objects.filter(id=pk).first()), availability='+')
    stistic = SchoolClass.objects.filter(id='{}'.format(pk))
    people = People.objects.filter(school_class='{}'.format(pk))
    return render(
        request,
        'app/state_list.html',
        context = {'state': state, 'cls':stistic, 'people':people})


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
        return render(
            request,
            'app/newwrite.html',
            context = {'form':form})
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
                    messages.error(request, 'Новые пароли не совпадают')
            else:
                messages.error(request, 'Старый пароль неверен!')
            
    else:
        form = PasrecForm()
    return render(
        request,
        'app/pasrec.html',
        {'form':form})


def image(request, pk):
    im = Image.open('app/static/img/{}.jpg'.format(pk), 'r')

    pix=im.load()
    w=im.size[0]
    h=im.size[1]
    width = []
    height = []
    for i in range(w):
        width.append(i)

    for i in range(h):
        height.append(i)

    return render(
        request,
        'app/image.html',
        {'w':width, 'h':height, 'pk':pk})
