from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Project, WeeklyReport
from django import forms
	

class ValidationSignUp(forms.ModelForm):
    email  = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(ValidationSignUp, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = {
        'username',
        'email',
        'password',
        'password_confirmation',
        }
    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(ValidationSignUp, self).save(commit=False)

        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()
            Profile.objects.create(user=instance, phone='', address='')

        return instance


class Login(forms.Form):
    user_cache = None
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(Login, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('invalid account!')
        else:
            self.user_cache = user


class EditForm(forms.ModelForm):
    first_name = forms.CharField(max_length =200)
    last_name = forms.CharField(max_length=200)
    birthdate = forms.DateField(widget=forms.TextInput(attrs={
        'id':'datepicker',
        'data-date-format':'yyyy-mm-dd',
        }),input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = Profile
        fields = {
        'first_name',
        'last_name',
        'position',
        'birthdate',
        'phone',
        'address'}

   
class WeeklyReports(forms.ModelForm):
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'data-date-format':'yyyy-mm-dd'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.FloatField(label='weekly hours')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.project = kwargs.pop('earvin',None)
        return super(WeeklyReports, self).__init__(*args, **kwargs)

    class Meta:
        model = WeeklyReport
        fields = '__all__'
        exclude ={'user','project_name'}
   
    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(WeeklyReports, self).save(commit=False)
        if commit:
            instance.user = self.user
            instance.project_name = self.project
            instance.save()
        return instance


class WeeklyReportsEdit(forms.ModelForm):
    title = forms.CharField(max_length = 2000)
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'data-date-format':'yyyy-mm-dd'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.FloatField(label='weekly hours')

    def clean_date_track(self):
        date_track = self.cleaned_data.get('date_track')
        return date_track
    class Meta:
        model = WeeklyReport
        fields ='__all__'
        exclude = {'user', 'project_name'}
        