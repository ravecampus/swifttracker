from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Project
from django import forms

# class SignUp(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['position','birthdate', 'phone', 'address']
		
class ValidationSignUp(forms.Form):
  
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise forms.ValidationError(u"Duplicate Username!, You can't proceed!")    
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise forms.ValidationError('Unmatch Password')
        return self.cleaned_data
    

class Login(forms.Form):
    user_cache = None
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('invalid account!')
        else:
            self.user_cache = user
        return self.cleaned_data


class EditForm(forms.Form):
    POSITION = (
        ('TRAINEE','trainee'),
        ('DEVELOPER','developer'),
        ('DESIGNER','designer'))

    first_name = forms.CharField(max_length =200)
    last_name = forms.CharField(max_length=200)
    position = forms.MultipleChoiceField(choices=POSITION)
    birthdate = forms.DateField(widget=forms.TextInput(attrs={
        'id':'datepicker',
        'data-date-format':'yyyy-mm-dd',
        }),input_formats=['%Y-%m-%d'])
    phone = forms.CharField(max_length=200)
    address =forms.CharField(max_length=200)

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        return birthdate    

class WeeklyReports(forms.Form):
    title = forms.CharField(max_length = 2000)
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'data-date-format':'yyyy-mm-dd'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.IntegerField(label='weekly hours')

    def clean_date_track(self):
        date_track = self.cleaned_data.get('date_track')
        return date_track