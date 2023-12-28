from django import forms
from .models import *

class AddPublicationForm( forms.ModelForm ):
    class Meta:
        model = Publication
        fields = ( 'text', )
    text = forms.CharField( label='', required=True, widget=forms.widgets.Textarea( attrs={'style': 'width:100%',}) )
