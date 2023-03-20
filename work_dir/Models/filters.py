from django.forms import MultipleChoiceField, SelectMultiple, forms
from django_filters import *
from django import forms


from .forms import AgeRangeWidget
from .models import *


class ModelFilter(FilterSet):
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город',
                      widget=forms.TextInput(attrs={'placeholder': 'Введите город'}))
    clothing_size = ChoiceFilter(choices=Model.CLOTHING_SIZE, label='Размер одежды', widget=forms.Select(attrs={'class': 'form-select'}))
    gender = ChoiceFilter(choices=Model.GENDER_CHOICES, label='Пол', widget=forms.Select(attrs={'class': 'form-select'}))
    age = RangeFilter(field_name='age', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Возраст')
    height = RangeFilter(field_name='height', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Рост')
    weight = RangeFilter(field_name='weight', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Вес')
    bust = RangeFilter(field_name='bust', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват груди')
    waist = RangeFilter(field_name='waist', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват талии')
    hips = RangeFilter(field_name='hips', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват бедер')
    shoe_size = RangeFilter(field_name='shoe_size', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(),
                            label='Размер ноги')
    BOOLEAN_CHOICES = [
        ('', 'Не важно'),
        (True, 'Да'),
        (False, 'Нет')
    ]
    tattoo = BooleanFilter(widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))
    in_under_photos = BooleanFilter(widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))
    nu_photos = BooleanFilter(widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))


    class Meta:
        model = Model
        fields = ['age', 'height', 'weight', 'bust', 'waist', 'hips', 'shoe_size', 'city', 'gender', 'clothing_size', 'tattoo', 'in_under_photos', 'nu_photos']


class PhotographerFilter(FilterSet):
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город', widget=forms.TextInput(attrs={'placeholder': 'Введите город'}))
    gender = ChoiceFilter(choices=Photographer.GENDER_CHOICES, label='Пол', widget=forms.Select(attrs={'class': 'form-select'}))
    genre = ModelMultipleChoiceFilter(field_name='genre', to_field_name='id', queryset=ShootingGenre.objects.all(), label='Жанр', widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}))
    tfp_photos = BooleanFilter(label='Сотрудничество по TFP', widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))
    in_under_photos = BooleanFilter(label='Согласие на фото в нижнем белье/купальнике', widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))
    nu_photos = BooleanFilter(label='Согласие на ню-фото (18+)', widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))

    class Meta:
        model = Photographer
        fields = ['city', 'gender', 'genre', 'tfp_photos', 'in_under_photos', 'nu_photos']

