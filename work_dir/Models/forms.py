from django import forms
from django.forms import Textarea

from .models import *

class CreateModel(forms.ModelForm):
    gender = forms.ChoiceField(choices=Model.GENDER_CHOICES, widget=forms.RadioSelect(), label='Пол')
    tattoo_description = forms.CharField(widget=Textarea(attrs={'cols': 60, 'rows': 10}))
    class Meta:
        model = Model
        # fields = ['name', 'surname', 'email', 'avatar', 'is_published']
        fields = '__all__'
class CreatePh(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = '__all__'

class AgeRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'От'}),
            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'До'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        else:
            return [None, None]

    def format_output(self, rendered_widgets):
        return '<div class="input-group">' + \
               '<div class="input-group-prepend">' + \
               '<span class="input-group-text">От</span>' + \
               '</div>' + \
               rendered_widgets[0] + \
               '<div class="input-group-append">' + \
               '<span class="input-group-text">До</span>' + \
               '</div>' + \
               rendered_widgets[1] + \
               '</div>'