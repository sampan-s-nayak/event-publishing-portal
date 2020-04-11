from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import Signup_form,User_creation_form
from common.models import UserData
from django.contrib.auth.models import User,Group


def SignUp(request):
    template_path = 'accounts/signup.html'
    if request.method == 'POST':
        f = User_creation_form(request.POST)
        if f.is_valid():
            user = f.save()
            new_user = authenticate(username=f.cleaned_data['username'],
                                    password=f.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('additional_info')

    
    form = User_creation_form()
    context = {'form': form}
    return render(request, template_path,context)

def additional_info(request):
    template_path = 'accounts/additional_info.html'
    if(request.method == 'POST'):
        f = Signup_form(request.POST)

        if f.is_valid():
            new_user = f.save()
            new_user.user=request.user
            new_user.save()
            
        return redirect('search')

    form = Signup_form()
    context = {'form':form}

    return render(request,template_path,context)

