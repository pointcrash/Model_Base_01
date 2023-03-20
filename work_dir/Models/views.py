from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django_filters.views import FilterView

from Models.filters import *
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
        return Model.objects.filter(is_published=True).order_by('time_create')


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
        return Photographer.objects.filter(is_published=True).order_by('time_create')


class StaffPage(FilterView):
    model = Stuff
    template_name = 'bootstrap/content.html'
    filterset_class = StaffFilter
    extra_context = {
        'title': 'Стилисты',
        'object': 'стилиста',
        'create': 'create_staff',
        'post': 'staff_post',
    }

    def get_queryset(self):
        return Stuff.objects.filter(is_published=True).order_by('time_create')



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


def show_staff_post(request, post_id):
    post = get_object_or_404(Stuff, pk=post_id)
    model_photos = ImageStuff.objects.filter(model=post)
    albums = Album.objects.filter(user=post.owner)
    type = post.type.values_list('name', flat=True)

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images') # get list of uploaded images
            for image in images:
                ImageStuff.objects.create(model=post, image=image) # create Image instance for each uploaded image
            return redirect('staff_post', post_id=request.user.stuff.pk)
    else:
        form = UploadImageForm()

    context = {
        'model_photos': model_photos,
        'post': post,
        'albums': albums,
        'user': request.user,
        'form': form,
        'type': type,
    }

    return render(request, 'bootstrap/staff_post.html', context=context)


@login_required
def create_model(request):
    owner_id = request.user.id
    if Model.objects.filter(owner_id=owner_id).exists():
        error_message = 'Модель уже зарегистрирован/а для данного пользователя'
        return render(request, 'bootstrap/create_ph.html', {'error_message': error_message})
    if request.method == 'POST':
        form = PhForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = request.user
            model.save()
            return redirect('ph_post', pk=model.pk)
    else:
        form = PhForm()
    return render(request, 'bootstrap/create_ph.html', {'form': form, 'context': 'модели'})

@login_required
def create_ph(request):
    owner_id = request.user.id
    if Photographer.objects.filter(owner_id=owner_id).exists():
        error_message = 'Фотограф уже зарегистрирован для данного пользователя'
        return render(request, 'bootstrap/create_ph.html', {'error_message': error_message})
    if request.method == 'POST':
        form = PhForm(request.POST, request.FILES)
        if form.is_valid():
            photographer = form.save(commit=False)
            photographer.owner = request.user
            photographer.save()
            return redirect('ph_post', pk=photographer.pk)
    else:
        form = PhForm()
    return render(request, 'bootstrap/create_ph.html', {'form': form, 'context': 'фотографа'})

@login_required
def create_staff(request):
    owner_id = request.user.id
    if Stuff.objects.filter(owner_id=owner_id).exists():
        error_message = 'Стилист уже зарегистрирован для данного пользователя'
        return render(request, 'bootstrap/create_ph.html', {'error_message': error_message})
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            stuff = form.save(commit=False)
            stuff.owner = request.user
            stuff.save()
            return redirect('staff_post', pk=stuff.pk)
    else:
        form = StaffForm()
    return render(request, 'bootstrap/create_ph.html', {'form': form, 'context': 'стилиста'})



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


@login_required
def delete_photo_staff(request, photo_id):
    photo = get_object_or_404(ImageStuff, pk=photo_id)
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
