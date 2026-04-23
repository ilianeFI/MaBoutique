from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from cart.models import Cart,CartItem
from requests import session

from .forms import LoginForm,RegisterForm
from django.contrib.auth import logout
from cart.views import get_or_create_cart
from django.contrib.auth.decorators import login_required
# Tu devras créer ce formulaire

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hachage sécurisé du mot de passe
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request,user)

            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    #on recuper le panier
    cart_id=request.session.get('cart_id')
    logout(request)

    if cart_id:
        request.session['cart_id']=cart_id
    return redirect('home')

