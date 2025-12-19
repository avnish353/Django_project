from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class CustRegistrationForm(UserCreationForm):
    country_code = forms.ChoiceField(
        choices=[
            ('+1', 'USA (+1)'),
            ('+91', 'India (+91)'),
            ('+44', 'UK (+44)'),
            ('+61', 'Australia (+61)'),      
        ],
        initial='+91',
        label="Country Code"
    )
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    
    class Meta:
        model=User
        fields=["first_name","last_name","email","country_code","mobile","username"]
 
class EmailForm(forms.Form):
    email = forms.EmailField()
 
        
class OTPPasswordResetForm(forms.Form):
    otp = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")