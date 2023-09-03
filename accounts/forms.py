from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from . import models
class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserChangeForm(UserChangeForm):
    class Meta:
        model = models.Profile
        fields = ('image', 'firstname', 'lastname', 'dob')

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields.pop('password')