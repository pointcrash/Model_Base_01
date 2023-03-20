import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from multiupload.fields import MultiFileField


# Create your models here.
class Model(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=250, null=True, verbose_name='Город')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')

    height = models.PositiveSmallIntegerField(verbose_name='Рост')
    weight = models.PositiveSmallIntegerField(verbose_name='Вес')
    bust = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват груди')
    waist = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват талии')
    hips = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват бедер')
    shoe_size = models.PositiveSmallIntegerField(blank=True, verbose_name='Размер ноги')
    CLOTHING_SIZE = [
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]
    clothing_size = models.CharField(max_length=4, choices=CLOTHING_SIZE, default='M', verbose_name='Размер одежды')

    hair_color = models.CharField(max_length=30, verbose_name='Цвет волос')
    eye_color = models.CharField(max_length=30, verbose_name='Цвет глаз')
    tattoo = models.BooleanField(default=True, verbose_name='Наличие тату')
    tattoo_description = models.CharField(max_length=200, blank=True,
                                          verbose_name='Если имеются тату, то на каких местах')

    in_under_photos = models.BooleanField(default=False, verbose_name='Согласие на фото в нижнем белье/купальнике')
    nu_photos = models.BooleanField(default=False, verbose_name='Согласие на ню-фото (18+)')
    tfp_photos = models.BooleanField(default=False, verbose_name='Сотрудничество по ТФП', null=True)

    avatar = models.ImageField(upload_to='avatar/model/%Y/%m/%d/', blank=True, verbose_name='Фото профиля')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Photographer(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=250, null=True, verbose_name='Город')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')

    genre = models.ManyToManyField('ShootingGenre')
    about = models.TextField(null=True, verbose_name='О себе')

    in_under_photos = models.BooleanField(default=False, verbose_name='Согласие на фото в нижнем белье/купальнике')
    nu_photos = models.BooleanField(default=False, verbose_name='Согласие на ню-фото (18+)')
    tfp_photos = models.BooleanField(default=False, verbose_name='Сотрудничество по ТФП', null=True)

    avatar = models.ImageField(upload_to='avatar/ph/%Y/%m/%d/', blank=True, verbose_name='Фото профиля')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

    # def __str__(self):
    #     return self.owner.username

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class ShootingGenre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name



class Stuff(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=250, null=True, verbose_name='Город')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')

    type = models.ManyToManyField('StuffType')

    tfp_photos = models.BooleanField(default=False, verbose_name='Сотрудничество по ТФП', null=True)

    avatar = models.ImageField(upload_to='avatar/stuff/%Y/%m/%d/', blank=True, verbose_name='Фото профиля')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

    # def __str__(self):
    #     return self.owner.username

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class StuffType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


# {{{{{{{    БЛОК ОБРАБОТКИ ФОТОГРАФИЙ       }}}}}}}}}}}}}}}

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.model.owner.username}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


#
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Альбом")
    time_create = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ImagePh(models.Model):
    model = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ImageStuff(models.Model):
    model = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# {{{{{{{{{{{         --------------          }}}}}}}}}}}}}}}
