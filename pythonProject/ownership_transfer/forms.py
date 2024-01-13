# ownership_transfer/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ownership,UserProfile
from django.contrib.auth.models import User
class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'name', 'mobile_number', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        user_profile = UserProfile.objects.create(user=user, mobile_number=self.cleaned_data['mobile_number'],
                                                  email=self.cleaned_data['email'])

        if commit:
            user_profile.save()

        return user

class OwnershipForm(forms.ModelForm):
    class Meta:
        model = Ownership
        fields = ['model','IMEI_Number','mobile_number', 'email']

    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    def __str__(self):
        return f"{self.model} {self.IMEI_Number} {self.mobile_number} {self.email}"

class OwnershipTransferForm(forms.Form):
    new_owner_username = forms.CharField(label='New Owner Username', max_length=100)