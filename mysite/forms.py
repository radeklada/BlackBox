from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

# formularz tworzenia nowych uzytkonikow
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

# formularze tworzenia kolejno nowej aplikacji, testu, kroku dla jakiegos testu

class NewApplicationForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=200)

class NewTestForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=200)
	result = forms.CharField(label='Rezultat', max_length=500)

class NewStepForm(forms.Form):
	description = forms.CharField(label="Opis", max_length=500)
	requirements = forms.CharField(label="Warunki poczatkowe", max_length=500)
	