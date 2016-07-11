from .forms import ValidationSignUp, Login, EditForm, WeeklyReports, WeeklyReportsEdit
from .models import Profile, Project, WeeklyReport
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .mixins import AuthViewMixins
from django.shortcuts import render
from django.conf import settings
import datetime
import calendar

# class based view
from django.views.generic import TemplateView



#class based
class HomeView(TemplateView):
    template_name = 'pages/home.html'
    context = {}
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)

        
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


#class based
class DashboardView(AuthViewMixins, TemplateView):
   
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
        

#class based
class EditProfileView(AuthViewMixins, TemplateView):
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


#class based
class ProjectView(AuthViewMixins, TemplateView):
    template_name = 'pages/projects.html'
    context = {}

    def get(self, *args, **kwargs):
        data = Project.objects.get(id=kwargs['project_id'])
        reports = WeeklyReport.objects.filter(project_name=data, user=self.request.user).order_by('-id')
        self.context['data'] = data
        self.context['reports'] = reports
        return render(self.request, self.template_name, self.context)


#class based
class AddReportView(AuthViewMixins, TemplateView):
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


#class based
class EditReportView(AuthViewMixins, TemplateView):
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


#class based
class LogoutView(TemplateView):
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('login'))
   

  