from .forms import ValidationSignUp, Login, EditForm, WeeklyReports, WeeklyReportsEdit
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, WeeklyReport
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
import datetime
# class based view
from django.views.generic import TemplateView

# function based
# def home_view(request):
#     return render(request, 'pages/home.html',{})

#class based
class HomeView(TemplateView):
    template_name = 'pages/home.html'
    context = {}
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)
# def signup_view1(request):
#     if request.method == "POST":
#         form = ValidationSignUp(request.POST)
#         if form.is_valid():
#             info = request.POST
        
#             user = User.objects.create(
#                 username = info['username'],
#                 email = info['email'])
#             user.set_password(info['password'])
#             user.save()
#             profile = Profile.objects.create(user=user, phone='', address='')
#             print(request.POST)
#             return HttpResponseRedirect(reverse('login'))
#         else:
#             return render(request, "pages/signup.html",{'form':form})
#     form = ValidationSignUp
#     return render(request, "pages/signup.html",{'form':form})

# class based 
class SignupView(TemplateView):
    template_name = 'pages/signup.html'
    context = {}

    def get(self, *args, **kwargs):
        self.context['form'] = ValidationSignUp()
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = ValidationSignUp(self.request.POST, request=self.request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))

        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

#function based

# function based
# def login_view(request):
#     form = Login()
#     if request.method == 'POST':
#         form = Login(request.POST)
#         if form.is_valid():
#             login(request, form.user_cache)
#             return HttpResponseRedirect(reverse('dashboard'))
#         else:
#             return render(request,'pages/login.html',{'form':form})
#     else:
#         return render(request, 'pages/login.html',{'form':form})


#class based
class LoginView(TemplateView):
    template_name = 'pages/login.html'
    context = {}

    def get(self, *args, **kwargs):
        self.context['form'] = Login()
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = Login(self.request.POST, request=self.request)
        if form.is_valid():
            login(self.request, form.user_cache)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            self.context['form'] = form
            return render(self.request, self.template_name, self.context)
        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

#function based

# @login_required(login_url='login')
# def dashboard_view(request):
#     if request.user.is_authenticated():
#         info = Profile.objects.get(user=request.user)
#         proj = Project.objects.filter(username=request.user)

#         if info.birthdate:
#              now = datetime.datetime.now()    
#              # profilebd = info.birthdate.year
#              age = int((datetime.date.today() - info.birthdate).days / 365.25  )

#              context = {'info':info,'proj':proj,'age':age}  
#              return render(request,'pages/dashboard.html', context)
#         else:
#             context = {'info':info,'proj':proj}
        
#             return render(request, 'pages/dashboard.html', context)
#     else:
#         return HttpResponseRedirect(reverse('login'))


#class based

class DashboardView(TemplateView):
   
    template_name = 'pages/dashboard.html'
    context = {}

    def get(self, *args, **kwargs):
        info = Profile.objects.get(user=self.request.user)
        projects = Project.objects.filter(username=self.request.user)
        if info.birthdate:
            age = int((datetime.date.today() - info.birthdate).days / 365.25 )
        else:
            self.context['info'] = info
            self.context['projects'] = projects
            return render(self.request, self.template_name, self.context)
        self.context['info'] = info
        self.context['projects'] = projects
        self.context['age'] = age
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            info = Profile.objects.get(user=self.request.user)
            projects = Project.objects.filter(username=self.request.user)

            self.context['info'] = info
            self.context['projects'] = projects
            return render(self.request, self.template_name, self.context)
        else:
            return HttpResponseRedirect(reverse('login'))
    
#function based

# @login_required(login_url='login')
# def edit_profile_view(request):
#     profile = Profile.objects.get(user=request.user)
#     form = EditForm(initial={
#         'first_name': request.user.first_name,
#         'last_name': request.user.last_name,
#         'birthdate': profile.birthdate,
#         'position' :profile.position,
#         'phone':profile.phone,
#         'address':profile.address})
    
#     if request.method == 'POST':
#         form = EditForm(request.POST)
#         if form.is_valid():

#             info = request.POST
#             user = User.objects.filter(username=request.user)
#             user.update(last_name = info['last_name'])
#             user.update(first_name = info['first_name'])
        
#             profile = Profile.objects.filter(user=request.user)
#             profile.update(
#                 position = info['position'],
#                 birthdate = info['birthdate'],
#                 phone = info['phone'],
#                 address = info['address']) 
#             return HttpResponseRedirect(reverse('dashboard'))
#         else:
#             return render(request, 'pages/edit_profile.html', {'form':form})

#     return render(request, 'pages/edit_profile.html', {'form':form})

#class based
class EditProfileView(TemplateView):
    template_name = 'pages/edit_profile.html'
    context = {}

    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)

        form = EditForm(instance=profile, initial={
            'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name
            })
        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        form = EditForm(self.request.POST, instance=profile)
        
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(id=self.request.user.id)
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            obj.save()
            user.save()

            return HttpResponseRedirect(reverse('dashboard'))
        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)

#funtion based
# @login_required(login_url='login')
# def project_view(request, project_id): 
#     data = Project.objects.get(id = project_id)
#     reports = WeeklyReport.objects.filter(project_name =data, user =request.user).order_by('-id')
#     return render(request ,'pages/projects.html',{'data':data, 'reports':reports })


#class based
class ProjectView(TemplateView):
    template_name = 'pages/projects.html'
    context = {}

    def get(self, *args, **kwargs):
        data = Project.objects.get(id=kwargs['project_id'])
        reports = WeeklyReport.objects.filter(project_name=data, user=self.request.user).order_by('-id')
        self.context['data'] = data
        self.context['reports'] = reports
        return render(self.request, self.template_name, self.context)

#function based 

# @login_required(login_url='login')
# def  add_report_view(request, project_id):
#     form = WeeklyReports()
#     if request.method == 'POST':
#         form = WeeklyReports(request.POST)
#         if form.is_valid():
#             info = request.POST
#             projects = Project.objects.get(id=project_id, username=request.user)
#             reports = WeeklyReport.objects.create(
#                 project_name = projects, 
#                 user = request.user,
#                 title = info['title'],
#                 date_track = info['date_track'],
#                 question1 = info['question1'],
#                 question2 = info['question2'],
#                 question3 = info['question3'],
#                 time_track = info['time_track']
#                 )
#             return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':project_id}))
#         else:
#             return render(request, 'pages/add_report.html', {'form':form})
#     return render(request, 'pages/add_report.html',{'form':form})

#class based
class AddReportView(TemplateView):
    template_name = 'pages/add_report.html'
    context = {}

    def get(self, *args, **kwargs):
        form = WeeklyReports()
        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'], username =self.request.user)
        user = self.request.user
        
        form = WeeklyReports(self.request.POST, user=user, earvin=project) #{'user':asdas, 'project_name': asdsa}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':kwargs['project_id']}))
        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)

#function based

# @login_required(login_url='login')
# def edit_report_view(request,project_id ,report_id):

#     project = WeeklyReport.objects.get(user=request.user ,id=report_id)
#     form = WeeklyReportsEdit(initial={
#         'title':project.title,
#         'date_track':project.date_track,
#         'question1':project.question1,
#         'question2':project.question2,
#         'question3':project.question3,
#         'time_track':project.time_track
#         })
#     if request.method == 'POST':
#         form = WeeklyReportsEdit(request.POST)
#         if form.is_valid():
#             info = request.POST
#             reports = WeeklyReport.objects.filter(id=report_id)
#             reports.update(title = project.title,
#             date_track = info['date_track'],
#             question1 = info['question1'],
#             question2 = info['question2'],
#             question3 = info['question3'],
#             time_track = info['time_track'])
#         return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':project_id}))
#     else:
#         return render(request, 'pages/edit_report.html',{'form':form})

#     return render(request, 'pages/edit_report.html',{'form':form})

#class based
class EditReportView(TemplateView):
    template_name = 'pages/edit_report.html'
    context = {}

    def get(self, *args, **kwargs):
        project = WeeklyReport.objects.get(user=self.request.user, id=kwargs['report_id'])
        form = WeeklyReportsEdit(instance=project)
        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        project = WeeklyReport.objects.get(id=kwargs['report_id'])
        form = WeeklyReportsEdit(self.request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':kwargs['project_id']}))
        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)

#function base

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('login'))

#class based
class LogoutView(TemplateView):
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('login'))
   

  