from django.shortcuts import render,render_to_response
from first_app.forms import UserProfileInfoForm,UserForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def special(request):
    if request.user.is_authenticated:
        return HttpResponse("You are logged in, Nice!")
    else:
        return render_to_response('first_app/login.html',{"message":'you need to be logged in order to visit the special page!'})

@login_required
def user_logut(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")


        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'first_app/login.html',{})






def index(request):
    return render(request,'first_app/index.html')

def Register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    registered=False

    if request.method =="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'first_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})

