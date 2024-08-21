from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model,hashers,logout

user = get_user_model()

#Class Based ViewsDa Qilingan Holati
class LoginView(View):
    template_name = 'login.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name,self.context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:messages.error(request,'Username or Password is incorrect')
        return redirect('/logins')

#Function Based ViewsDa Qilingan Holati
# def logins(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:messages.error(request, 'Username or Password is incorrect')
#     return render(request, 'login.html')

class RegisterView(View):
    template_name = 'register.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name,self.context)


    def post(self, request):
        last_name = request.POST.get('lastname')
        first_name = request.POST.get('firstname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('/registered')
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
                return redirect('/registered')
            else:
                user = User.objects.create(
                last_name=last_name,
                first_name=first_name,
                email=email,
                username=username,
                password=hashers.make_password(confirm_password))
                user.save()
                return redirect('/logins')
        else:messages.error(request,"Passwords do not match")
        return redirect('/registered')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/logins')
