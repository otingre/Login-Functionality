from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from login_page import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            message.error(request, "Username already exists, p[ease enter a new one")
            return redirect('home')

        if User.objects.filter(email=email):
            message.error(request, "Email already exists, p[ease enter a new one")
            return redirect('home')

        if len(username) > 10:
            message.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            message.error(request, "Passwords did not match")

        if not username.isalnum() :
            message.error(request, "Username should be Alpha-Numeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been sucessfully created.")

        # Welcome Email

        subject = "Welcome to my page"
        message = "Hello" + myuser.first_name + "!! \n" + "Please confrim your email for activation \n" + "Thankyou " + myuser.first_name
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)

        return redirect('signin')
    
    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        
        else:
            messages.error(request, "Wrong username or password")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):

    logout(request)
    messages.success(request, "Logged out sucessfully")
    return redirect('home')
