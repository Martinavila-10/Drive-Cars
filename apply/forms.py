from django import forms

class crearForms(forms.Form):
    titulo = forms.CharField(label='Nombre', max_length=200)
    descripcion = forms.CharField(label='Descripción',widget=forms.Textarea)