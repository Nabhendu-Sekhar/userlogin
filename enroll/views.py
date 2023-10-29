from django.shortcuts import render
from enroll.forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.http import HttpResponseRedirect
# Create your views here.



#user signup function

def sign_up(request):
    if request.method == 'POST':
        fm=SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Your account has been created Sucessfully !!')
    else:
        fm=SignupForm()
    return render (request,'enroll/signup.html',{'form':fm})



# user login function

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                messages.success(request,'Successfully loged in your account')
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/profile/')
        else:
            fm=AuthenticationForm()
        return render(request,'enroll/userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')



#userprofile function

def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'enroll/profile.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')



#logout form function

def user_logouot(request):
    logout(request)
    messages.success(request,'Log out Successfully')        
    return HttpResponseRedirect('/login/')

#password change with only two confirmation password

def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm=SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'Password changed sucessfully !!')
                return HttpResponseRedirect('/profile/')
        else:
            fm=SetPasswordForm(user=request.user)
        return render(request,'enroll/changepass1.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
