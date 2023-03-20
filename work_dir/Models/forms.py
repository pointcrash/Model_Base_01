from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Textarea
from multiupload.fields import MultiImageField

from .models import *


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].error_messages = {'required': 'Please enter your email address.'}
        self.fields['first_name'].error_messages = {'required': 'Please enter your first name.'}
        self.fields['last_name'].error_messages = {'required': 'Please enter your last name.'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label='Пароль', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class CreateModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['city', 'age', 'gender', 'height', 'weight', 'bust', 'waist', 'hips', 'shoe_size',
                  'clothing_size', 'hair_color', 'eye_color', 'tattoo', 'tattoo_description', 'in_under_photos',
                  'nu_photos', 'tfp_photos', 'avatar', 'is_published']

        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'bust': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control'}),
            'shoe_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'clothing_size': forms.Select(attrs={'class': 'form-control'}),
            'hair_color': forms.TextInput(attrs={'class': 'form-control'}),
            'eye_color': forms.TextInput(attrs={'class': 'form-control'}),
            'tattoo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tattoo_description': forms.TextInput(attrs={'class': 'form-control'}),
            'in_under_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nu_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tfp_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PhForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = ['city', 'age', 'gender', 'genre', 'about', 'in_under_photos', 'nu_photos', 'tfp_photos', 'avatar', 'is_published']

    city = forms.CharField(
        label='Город',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    age = forms.IntegerField(
        label='Возраст',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        label='Пол',
        choices=Photographer.GENDER_CHOICES,
        initial='M',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    genre = forms.ModelMultipleChoiceField(
        label='Жанр фотосъемки',
        queryset=ShootingGenre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'})
    )

    about = forms.CharField(
        label='О себе',
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        required=False
    )

    in_under_photos = forms.BooleanField(
        label='Согласие на фото в нижнем белье/купальнике',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    nu_photos = forms.BooleanField(
        label='Согласие на ню-фото (18+)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    tfp_photos = forms.BooleanField(
        label='Сотрудничество по ТФП',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    avatar = forms.ImageField(
        label='Фото профиля',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    is_published = forms.BooleanField(
        label='Опубликовать',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


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


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['images']