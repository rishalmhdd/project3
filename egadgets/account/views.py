from django.forms import BaseModelForm
from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import LoginForm,RegForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.generic import TemplateView,FormView,CreateView


# Create your views here.


# class LandingView(View):
#     def get(self,request):
#         return render(request,"landing.html")

class LandingView(TemplateView):
    template_name='landing.html'
    


    
class LoginView(FormView):
    template_name='login.html'
    form_class=LoginForm

    # def get(self,request):
    #     form=LoginForm()
    #     return render(request,'login.html',{"form":form}) 


    
    def post(self,request):
        formdata=LoginForm(data=request.POST)
        if formdata.is_valid():
            uname=formdata.cleaned_data.get('username')
            pswd=formdata.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Login Failed!!....Invaild username/password!!")
                return redirect('login')
        return redirect(request,"login.html",{"form":formdata}) 

# class RegView(View):
#     def get(self,request):
#         form=RegForm()
#         return render(request,'reg.html',{"form":form})  
#     def post(self,request):
#         formdata=RegForm(data=request.POST)
#         if formdata.is_valid():
#             formdata.save()
#             messages.success(request,"Registration succefull!!!")
#             return redirect('log')
#         messages.error(request,"Registration Failed!") 
#         return render(request,'reg.html',{"form":formdata}) 

class RegView(CreateView):
    template_name='reg.html'
    form_class=RegForm
    success_url=reverse_lazy('login')


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('landing')       

    def form_valid(self,form):
        messages.success(self.request,"User Registration Compltetd")
        return super().form_valid(form) 
    def form_invalid(self,form):
        messages.error(self.request,"Registration Failed!!")
        return super().form_invalid(form)
    