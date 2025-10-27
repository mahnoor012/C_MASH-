from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'profession', 'address', 'country', 'github', 'linkedin','facebook','whatsapp', 'profile_picture']



from .models import Website
from urllib.parse import urlparse


from django import forms
from .models import Website
from urllib.parse import urlparse

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Codeforces', 'class': 'input'}),
            'url': forms.URLInput(attrs={'placeholder': 'https://codeforces.com', 'class': 'input'}),
        }

    def clean_url(self):
        url = (self.cleaned_data.get('url') or '').strip()
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url.lstrip('/')
        return url

