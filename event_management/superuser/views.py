from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required
def home(request):
    return render(request,'superuser/addmod.html')

@login_required
def add_mod(request):
    user_name = request.POST['username']
    cpassword = request.POST['cpassword']
    firstname = request.POST['fname']
    lastname = request.POST['lname']
    email = request.POST['email']
    user = User.objects.create_user(username = user_name,first_name=firstname, last_name = lastname, email = email, password = cpassword,is_staff=True)
    user.save()
    messages.info(request, "Successfully Created")
    return redirect("/superuser/home")    

@login_required
def display(request):
    users = User.objects.filter(is_staff=True)
    return render(request,'superuser/display.html',{'key': users})

@login_required
def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.info(request,"Successfully Deleted")
    return redirect("/superuser/display")    