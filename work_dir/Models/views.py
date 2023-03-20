import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, FormView
from django_filters.views import FilterView

from Models.filters import ModelFilter, PhotographerFilter
from Models.forms import *
from Models.models import *


def home(request):
    return render(request, 'bootstrap/homepage.html')


@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'bootstrap/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'bootstrap/edit_profile.html', {'form': form})


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'bootstrap/register.html'
    success_url = reverse_lazy('models')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('models')


class CustomLoginView(LoginView):
    template_name = 'bootstrap/login.html'
    form_class = LoginForm
    success_url = '/home'


def logout_user(request):
    logout(request)
    return redirect('login')


class ModelsPage(FilterView):
    model = Model
    template_name = 'bootstrap/content.html'
    filterset_class = ModelFilter
    extra_context = {
        'title': 'Модели',
        'object': 'модели',
        'create': 'create_model',
        'post': 'model_post',
    }
    def get_queryset(self):
        return Model.objects.filter(is_published=True)


class PhotographerPage(FilterView):
    model = Photographer
    template_name = 'bootstrap/content.html'
    filterset_class = PhotographerFilter
    extra_context = {
        'title': 'Фотографы',
        'object': 'фотографа',
        'create': 'create_ph',
        'post': 'ph_post',
    }

    def get_queryset(self):
        return Photographer.objects.filter(is_published=True)


class PhotographerPage(FilterView):
    model = Photographer
    template_name = 'bootstrap/content.html'
    filterset_class = PhotographerFilter
    extra_context = {
        'title': 'Стилисты',
        'object': 'стилиста',
        'create': 'create_ph',
        'post': 'staff_post',
    }

    def get_queryset(self):
        return Photographer.objects.filter(is_published=True)



def show_model_post(request, post_id):
    post = get_object_or_404(Model, pk=post_id)
    model_photos = Image.objects.filter(model=post)
    albums = Album.objects.filter(user=post.owner)

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images') # get list of uploaded images
            for image in images:
                Image.objects.create(model=request.user.model, image=image) # create Image instance for each uploaded image
            return redirect('model_post', post_id=request.user.model.pk)
    else:
        form = UploadImageForm()

    context = {
        'model_photos': model_photos,
        'post': post,
        'albums': albums,
        'user': request.user,
        'form': form,
    }

    return render(request, 'bootstrap/model_post.html', context=context)

def show_ph_post(request, post_id):
    post = get_object_or_404(Photographer, pk=post_id)
    model_photos = ImagePh.objects.filter(model=post)
    albums = Album.objects.filter(user=post.owner)
    genres = post.genre.values_list('name', flat=True)

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images') # get list of uploaded images
            for image in images:
                ImagePh.objects.create(model=post, image=image) # create Image instance for each uploaded image
            return redirect('ph_post', post_id=request.user.photographer.pk)
    else:
        form = UploadImageForm()

    context = {
        'model_photos': model_photos,
        'post': post,
        'albums': albums,
        'user': request.user,
        'form': form,
        'genres': genres,
    }

    return render(request, 'bootstrap/ph_post.html', context=context)


@login_required
def model_form_view(request):
    if request.method == 'POST':
        form = CreateModelForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the user already has a model card
            if Model.objects.filter(owner=request.user).exists():
                messages.error(request, 'У вас уже есть карточка модели')
                return redirect(reverse_lazy('create_model'))

            try:
                # Save the model object
                model = form.save(commit=False)
                model.owner = request.user
                model.save()
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'Произошла ошибка при сохранении модели')
                return redirect(reverse_lazy('create_model'))
    else:
        form = CreateModelForm()

    context = {'form': form}
    return render(request, 'bootstrap/create_model.html', context)

@login_required
def create_ph(request):
    if request.method == 'POST':
        form = PhForm(request.POST, request.FILES)
        if form.is_valid():
            photographer = form.save(commit=False)
            photographer.owner = request.user
            photographer.save()
            return redirect('ph_post', pk=photographer.pk)
    else:
        form = PhForm()
    return render(request, 'bootstrap/create_ph.html', {'form': form})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Image, pk=photo_id)
    if photo.model.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Вы не можете удалить эту фотографию'})
    photo.delete()
    return JsonResponse({'status': 'ok', 'message': 'Фотография успешно удалена'})

@login_required
def delete_photo_ph(request, photo_id):
    photo = get_object_or_404(ImagePh, pk=photo_id)
    if photo.model.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Вы не можете удалить эту фотографию'})
    photo.delete()
    return JsonResponse({'status': 'ok', 'message': 'Фотография успешно удалена'})

def create_album(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        Album.objects.create(title=title, user=request.user)
        albums = Album.objects.filter(user=request.user)
        return render(request, 'post', {'albums': albums, "post_id": request.user.model.pk})
    return JsonResponse({'error': 'Invalid request'})
