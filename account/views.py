from django.contrib.auth.models import User, auth
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as userLogin


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'SignUp.html')

def storeSignUp(request):
    return render(request, 'storeSignup.html')


def login(request):
    return render(request, 'login.html') 


def createAccount(request):
    if request.method == 'POST':
        fName = request.POST['firstName']
        lName = request.POST['lastName']
        phone = request.POST['phoneNumber']
        email = request.POST['email']
        password = request.POST['password']
        proPic = request.FILES['imageUpload']

        message1 = 'Account already exists with this Phone Number! Please use a different one.'

        if uniquePhoneNumber(phone):
            username = uniqueUsername(first_name=fName, last_name=lName)

            user = User.objects.create_user(username=username, first_name=fName, last_name=lName, email=email, password=password)
            user.save()

            user.profile.image = proPic
            user.profile.phone = phone
            user.save()
            user.profile.save()

            return render(request, 'wellcomePage.html', {'username': username})
        else:
            messages.info(request, message1)
            return redirect('signup')
    else:
        return render(request, 'SignUp.html')
    
    
def createStore(request):
    if request.method == 'POST':
        fname = request.POST['ownerName']
        storeName = request.POST['storeName']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        proPic = request.FILES['imageUpload']

        userName = uniqueUsername(fname)
        
        if uniquePhoneNumber(phone):
            user = User.objects.create_user(username=userName, first_name=fname, email=email, password=password)
            user.save()
            
            user.profile.isStore = True
            user.profile.storeName = storeName
            user.profile.phone = phone
            user.profile.image = proPic
            user.profile.save()
            user.save()
            return render(request, 'wellcomePage.html', {'username': userName})
        else:
            message1 = 'Account already exists with this Phone Number! Please choose a different one.'
            messages.info(request, message1)
            return redirect('signup')
    else:
        return render(request, 'SignUp.html')
        


def uniquePhoneNumber(phoneNumber):
    try:
        Profile.objects.get(phone=phoneNumber)
        return False
    except Profile.DoesNotExist:
        return True
    
    
def isPhoneNumber(user_input):
    return not any(char.isalpha() for char in user_input)


def uniqueUsername(first_name = '', last_name = ''):
    users = User.objects.all()
    usernames = [user.username for user in users]

    username_base = f"{first_name.lower().replace(' ', '')}{last_name.lower().replace(' ', '')}"
    username = username_base

    if not usernames:
        return username

    counter = 0
    while username in usernames:
        username = username_base + str(counter)
        counter += 1

    return username





def logOutUser(request):
    auth.logout(request)
    return redirect('index')


def loginUser(request):
    if request.method == 'POST':
        phone = request.POST['phoneNumber']
        password = request.POST['password']

        if isPhoneNumber(phone):
            
            try:
                pro = Profile.objects.get(phone=phone)
                user = pro.user
            except Profile.DoesNotExist:
                user = None
                    
            if user is not None:
                if user.check_password(password):
                    userLogin(request, user)
                    return redirect('storeHome')
            else:
                messages.info(request, 'User do not exist. Please Signup')
                return redirect('signup')
        else:
            user = auth.authenticate(username=phone, password=password)
            if user is not None:
                userLogin(request, user)
                return redirect('storeHome')
            else:
                messages.info(request, 'User do not exist. Please Signup')
                return redirect('signup')
