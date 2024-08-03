# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Message, Contact
from .forms import MessageForm
from .models import Message, User

def home(request):
    return render(request, 'app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'app/contact_list.html', {'contacts': contacts})

@login_required
def message_list(request):
    contacts = User.objects.exclude(id=request.user.id)  # Все пользователи, кроме текущего
    selected_contact_id = request.GET.get('contact_id')
    selected_contact = User.objects.filter(id=selected_contact_id).first() if selected_contact_id else None
    messages = Message.objects.filter(sender=request.user, receiver=selected_contact) | \
               Message.objects.filter(sender=selected_contact, receiver=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'app/message_list.html', {
        'contacts': contacts,
        'selected_contact': selected_contact,
        'messages': messages
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'app/send_message.html', {'form': form})

@login_required
def switch_user(request):
    # Логика для смены пользователя
    return redirect('home')
