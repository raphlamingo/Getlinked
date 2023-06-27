from django.shortcuts import render, redirect
from .models import Jobs
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, JobForm
from django.contrib import messages
from django.template import RequestContext
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def home(request):
    job= Jobs.objects.all()
    paginator = Paginator(job, 2)
    try:
        page = request.GET.get('page')
        job= paginator.page(page)
    except PageNotAnInteger:
        page=1
        job= paginator.page(page)
    except EmptyPage:
        page= paginator.num_pages
        job= paginator.page(page)
    if job.has_next():
        next_page_number = job.next_page_number()
        next_page = paginator.get_page(next_page_number)
    else:
        next_page = None
    return render(request,'index.html',{'jobs':job, 'next_page': next_page})

def loginuser(request):
    req= 'login'
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        try:
            user= User.objects.get(username= username)
        except:
            messages.error(request, 'User doesnt exist')
            return redirect('register')
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password')
    return render(request,'login.html',{'context':req})

def register(request):
    req= 'register'
    form= CustomUserCreationForm()
    if request.method == 'POST':
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    return render(request,'login.html',{'context':req, 'form':form} )

def logoutuser(request):
    logout(request)
    return redirect('home')

def find(request):
    search_query= request.GET.get('query')
    job= Jobs.objects.filter(title__icontains=search_query).order_by('date_posted')
    paginator = Paginator(job, 2)
    try:
        page = request.GET.get('page')
        job= paginator.get_page(page)
    except PageNotAnInteger:
        page=1
        job= paginator.get_page(page)
    except EmptyPage:
        page= paginator.num_pages
        job= paginator.get_page(page)
    if job.has_next():
        next_page_number = job.next_page_number()
        next_page = paginator.get_page(next_page_number)
    else:
        next_page = None
    return render(request,'index.html', {'jobs':job, 'next_page': next_page })

@login_required(login_url='login_user')
def user(request):
    logged= request.user
    jobs= Jobs.objects.filter(author=logged)
    return render(request,'profile.html',{'post':jobs,'user':logged})

@login_required(login_url='login_user')
def new(request):
    req= 'new job'
    form= JobForm()
    if request.method == 'POST':
        form= JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user= request.user)
            return redirect('home')
    return render(request,'login.html',{'context':req, 'form':form})

def post(request,pk):
    job= Jobs.objects.get(id=pk)
    return render(request, 'single.html',{'post':job})

@login_required(login_url='login_user')
def delete(request,pk):
    post= Jobs.objects.get(id=pk)
    if request.method== "POST":
        post.delete()
        return redirect('home')
    return render( request, 'delete.html')

@login_required(login_url='login_user')
def update(request, pk):
    req= 'new job'
    post= Jobs.objects.get(id=pk)
    form= JobForm(instance=post)
    if request.method == 'POST':
        new_update= JobForm(request.POST, instance=post)
        if new_update.is_valid():
            new_update.save()
            return redirect('home')
    return render(request, 'login.html', {'form':form,'context':req})
