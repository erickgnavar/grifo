from django.forms import ModelForm
from django import forms
from models import *

class ContactoForm(forms.Form):
	corre = forms.EmailField(label='Tu correo aqui')
	mensaje = forms.CharField(widget=forms.Textarea)

class GriferoForm(ModelForm):
	class Meta:
		model = Grifero

class PreciosForm(forms.Form):
	pass