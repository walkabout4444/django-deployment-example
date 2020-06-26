from django.shortcuts import render
from basicapp.forms import UserForm, UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context_dict = {"text": 'INDEX view loaded from basicapp.views'}
    return render(request, 'basicapp/index.html', context_dict)

def other(request):
    context_dict = {"text": 'OTHER view loaded from basicapp.views.'}
    return render(request, 'basicapp/other.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('You are logged in!')

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print(f"Logged in: {username} using password: {password}")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'basicapp/login.html', {})

def registration(request):

    registered = False
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Do something
            user = user_form.save(commit=True)
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered }
    return render(request, 'basicapp/registration.html', context_dict)
