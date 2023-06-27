from django.forms import ModelForm, DateField,DateInput,CharField,PasswordInput,TextInput,BooleanField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Jobs

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields=['email','password1','password2','username']

class JobForm(ModelForm):
    date_due = DateField(widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model= Jobs
        fields=['title','company','description','pay','requirement','company_logo','date_due']

    def save(self, commit=True, user=None):
        instance = super(JobForm, self).save(commit=False)
        if user:
            instance.author = user
        if commit:
            instance.save()
        return instance