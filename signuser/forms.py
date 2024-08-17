from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'class':'form-control form-control-lg'
        })
        self.fields['password1'].widget.attrs.update({
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'class':'form-control form-control-lg'
        })
        self.fields['password2'].widget.attrs.update({
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'class':'form-control form-control-lg'
        })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']