from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django_filters.views import FilterView

from Models.filters import ModelFilter
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

menu = [
    {'title': "Модели", 'url_name': 'models'},
    # {'title': "Фотографы", 'url_name': 'photographers'},
    # {'title': "Дополнительно", 'url_name': 'stuff'},
    # {'title': "Фото", 'url_name': 'view_photos'},
    # {'title': "Локации", 'url_name': 'locations'},
    # {'title': "Галерея", 'url_name': 'gallery'},
    # {'title': "Войти", 'url_name': 'entry'}
]

class ModelsPage(FilterView):
    model = Model
    create = 'create_model'
    template_name = 'bootstrap/content.html'
    filterset_class = ModelFilter
    extra_context = {'title': 'Модели'}

class PhotographerPage(ListView):
    model = Photographer
    menu = menu
    create = 'create_ph'
    template_name = 'models/content.html'
    context_object_name = "posts"
    extra_context = {'menu': menu, 'create': create, 'title': 'Фотографы'}

    def get_queryset(self):
        return Photographer.objects.filter(is_published=True)

def show_post(request, post_id):
    post = get_object_or_404(Model, pk=post_id)
    fields = post._meta.get_fields()

    context = {
        # 'fields': fields,
        'post': post,
        'menu': menu,
        # 'title': post.owner,
    }

    return render(request, 'bootstrap/post.html', context=context)

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

    # @receiver(pre_save, sender=Model)
    # def set_owner(sender, instance, **kwargs):
    #     if not instance.pk:  # Если это новый объект, то заполняем поле owner
    #         instance.owner = instance.user

class CreatePh(CreateView):
    form_class = CreatePh
    menu = menu
    template_name = 'models/create_ph.html'
    extra_context = {'menu': menu, 'title': 'Модели'}


@login_required
def view_photos(request):
    photos = Photo.objects.all()
    # filter(owner=request.user)
    return render(request, 'models/photos.html', {'photos': photos})


@method_decorator(login_required, name='dispatch')
class UploadPhotosView(View):
    template_name = 'models/upload_photos.html'

    def get(self, request):
        form = PhotoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            return redirect('view_photos')
        return render(request, self.template_name, {'form': form})

