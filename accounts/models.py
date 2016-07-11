from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Profile(models.Model):
    TRAINEE = 'TRAINEE'
    DEVELOPER = 'DEVELOPER'
    DESIGNER = 'DESIGNER'
    POSITION = (
        (TRAINEE,'trainee'),
        (DEVELOPER,'developer'),
        (DESIGNER,'designer')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    position = models.CharField(max_length=2000, choices=POSITION)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11,null=True, blank=True)
    address = models.CharField(max_length=120,null=True, blank=True)
   

    def __str__(self):
        return str(self.user)

class Project(models.Model):
    TRAINEE = 'TRAINEE'
    DEVELOPER ='DEVELOPER'
    DESIGNER = 'DESIGNER'
    POSITION = (
        (TRAINEE,'trainee'),
        (DEVELOPER,'developer'),
        (DESIGNER,'designer')
    )
    username = models.ManyToManyField(User) 
    name = models.CharField(max_length=2000) 
    position = models.CharField(max_length=2000, choices=POSITION, default=TRAINEE)
    weekly_hours = models.IntegerField()  

    def __str__(self):
        return "{}".format(self.name)

class WeeklyReport(models.Model):
    
    project_name = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=120)
    date_track= models.DateField(null=True, blank=True)
    question1 = models.CharField(max_length=2000)
    question2 = models.CharField(max_length=2000)
    question3 = models.CharField(max_length=2000)
    time_track = models.FloatField(max_length=2000,null=True, blank=True)

    def __str__(self):
        return "{}".format(self.project_name)
