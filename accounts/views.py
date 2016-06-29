from .forms import ValidationSignUp, Login, EditForm, WeeklyReports
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, WeeklyReport
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.shortcuts import render
from django.conf import settings
import datetime

def home_view(request):
    return render(request, 'pages/home.html',{})

def signup_view(request):
    if request.method == "POST":
        form = ValidationSignUp(request.POST)
        if form.is_valid():
            info = request.POST
        
            user = User.objects.create(
                username = info['username'],
                email = info['email'])
            user.set_password(info['password'])
            user.save()

            # name = User.objects.get(username =info['username'])
            profile = Profile.objects.create(user=user, position='', phone='', address='')

            print(request.POST)
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, "pages/signup.html",{'form':form})
    form = ValidationSignUp
    return render(request, "pages/signup.html",{'form':form})


def login_view(request):
    form = Login()
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,'pages/login.html',{'form':form})
    else:
        return render(request, 'pages/login.html',{'form':form})

@login_required(login_url='login')
def dashboard_view(request):
    if request.user.is_authenticated():
        info = Profile.objects.get(user=request.user)
        proj = Project.objects.filter(username=request.user)
        if info.birthdate:
             now = datetime.datetime.now()    
             profilebd = info.birthdate.year
             current_year = now.year
             # age = current_year - profilebd
             age = now - timedelta(profilebd)
             context = {'info':info,'proj':proj,'age':age}  
             return render(request,'pages/dashboard.html', context)
        else:
            context = {'info':info,'proj':proj}
        
            return render(request, 'pages/dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))
@login_required(login_url='login')
def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)
   

    form = EditForm(instance=profile, initial={'first_name': request.user.first_name}) 
    if request.method == 'POST':
        # user_id = request.GET.get('id')
        form = EditForm(request.POST)
        if form.is_valid():

            info = request.POST
            user = User.objects.filter(username=request.user)
            user.update(last_name = info['last_name'])
            user.update(first_name = info['first_name'])
        
            profile = Profile.objects.filter(user=request.user)
            profile.update(position = info['position'],
                birthdate = info['birthdate'],
                phone = info['phone'],
                address = info['address']) 
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'pages/edit_profile.html', {'form':form})

    return render(request, 'pages/edit_profile.html', {'form':form})

# def edit_profile_again(request):
# 
@login_required(login_url='login')
def project_view(request, project_id): 
    data = Project.objects.get(id = project_id)

    
    
    reports = WeeklyReport.objects.filter(project_name =data, user =request.user)
    # form = ProjectQuery(request.GET)
    # if form.is_valid():
    #     info = request.GET

    # else:
    #     return render(request, 'pages/project.html',{})
    return render(request ,'pages/projects.html',{'data':data, 'reports':reports })
 

@login_required(login_url='login')
def  add_report_view(request, project_id):
    form = WeeklyReports()
    if request.method == 'POST':
        form = WeeklyReports(request.POST)
        if form.is_valid():
            info = request.POST
            projects = Project.objects.get(id=project_id)
            reports = WeeklyReport.objects.create(
                project_name = projects, 
                user = request.user,
                title = info['title'],
                date_track = info['date_track'],
                question1 = info['question1'],
                question2 = info['question2'],
                question3 = info['question3'],
                time_track = info['time_track']
                )
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':project_id}))
        else:
            return render(request, 'pages/add_report.html', {'form':form})

    return render(request, 'pages/add_report.html',{'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


  