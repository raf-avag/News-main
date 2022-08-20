from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, DetailView, UpdateView

from .forms import NewUserForm
from .models import News, Category



def home(request):
    search_query = request.GET.get('q', '')
    if search_query:
        all_news = News.objects.filter(title__icontains=search_query)
    else:
        all_news = News.objects.all().order_by('-add_time')
    paginator = Paginator(all_news, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'home.html', {'all_news': page})


# Detail Page


# Fetch all category


def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html', {
'cats': cats})


# Fetch all category
def category(request, id):
    category = Category.objects.get(id=id)
    news = News.objects.filter(category=category)
    paginator = Paginator(news, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'category-news.html', { 'all_news': page,'category': category})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="accounts/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


class DescriptionDelete(DeleteView):
    model = News
    context_object_name = 'home'
    success_url = reverse_lazy('home')


class DescriptionCreate(CreateView):
    model = News
    fields = ['detail', 'title', 'image', 'category']
    success_url = reverse_lazy('home')


class DescriptionDetail(DetailView):
    model = News


class DescriptionUpdate(UpdateView):
    model = News
    fields = ['name']
    success_url = reverse_lazy('home')

def simple_upload(request):
   if request.method == 'POST' and request.FILES['image']:
      image = request.FILES['image']