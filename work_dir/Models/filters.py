from django.forms import MultipleChoiceField, SelectMultiple
from django_filters import FilterSet, RangeFilter, BooleanFilter

from .forms import AgeRangeWidget
from .models import *


class ModelFilter(FilterSet):

    clothing_size = MultipleChoiceField(choices=Model.CLOTHING_SIZE, widget=SelectMultiple, label='Размер одежды')
    gender = MultipleChoiceField(choices=Model.GENDER_CHOICES, widget=SelectMultiple, label='Пол')
    age = RangeFilter(field_name='age', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Возраст')
    height = RangeFilter(field_name='height', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Рост')
    weight = RangeFilter(field_name='weight', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Вес')
    bust = RangeFilter(field_name='bust', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват груди')
    waist = RangeFilter(field_name='waist', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват талии')
    hips = RangeFilter(field_name='hips', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват бедер')
    shoe_size = RangeFilter(field_name='shoe_size', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(),
                            label='Размер ноги')
    tattoo = BooleanFilter()
    in_under_photos = BooleanFilter()
    nu_photos = BooleanFilter()

    class Meta:
        model = Model
        fields = ['age', 'height', 'weight', 'bust', 'waist', 'hips', 'shoe_size', 'gender', 'clothing_size', 'tattoo', 'in_under_photos', 'nu_photos']
