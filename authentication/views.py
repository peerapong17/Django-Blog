from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout



def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        # username = request.POST['username']
        # email = request.POST['email']
        # password = request.POST['password']
        # confirmPassword = request.POST['confirmPassword']
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "This email already in-use")
        # elif password != confirmPassword:
        #     messages.error(request, "Password does not match")
        # else:
        #     user = User.objects.create_user(
        #         username=username,
        #         email=email,
        #         password=password
        #     )
        #     user.save()
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Create account success")
            return redirect("loginUser")

    return render(request, "auth/register.html", {"form": form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.error(request, "User with given email does not exist")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('registerUser')

    return render(request, "auth/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('loginUser')
