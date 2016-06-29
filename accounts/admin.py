from django.contrib import admin
from .forms import SignUp
from .models import Profile, Project, WeeklyReport

class ProjectUser(admin.ModelAdmin):
    list_display = ['name', 'position', 'weekly_hours']
    filter_horizontal = ['username']
    class Meta:
        model = Project

admin.site.register(Project, ProjectUser)

class ProfileUser(admin.ModelAdmin):
    list_display = ['user','position','birthdate','phone', 'address']
    form = SignUp
    # class Meta:
    #     model = Profile
 
admin.site.register(Profile, ProfileUser)


class WeeklyReportUser(admin.ModelAdmin):
    list_display = ['project_name', 'title', 'date_track', 'question1', 'question2', 'question3', 'time_track']
    class Meta:
        model = WeeklyReport

admin.site.register(WeeklyReport, WeeklyReportUser)