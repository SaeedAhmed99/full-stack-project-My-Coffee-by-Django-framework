from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
import re
from django.contrib import auth
from products.models import Product


def login(request):
    if request.method == 'POST' and 'btnsignin' in request.POST :
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            print(request.POST)
            if 'remembercheck' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            # messages.success(request, 'You are now logged in')
        else:
            messages.error(request, 'Username or Password invalid')
        return redirect('login')
    else:
        return render(request, 'accounts/signin.html', {})

def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        fname = None
        lname = None
        address1 = None
        address2 = None
        city = None
        state = None
        zip = None
        email = None
        username = None
        password = None
        agreecheck = None
        is_added = None

        # Get Data From Form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in first name field')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in last name field')

        if 'address1' in request.POST: address1 = request.POST['address1']
        else: messages.error(request, 'Error in address1 field')

        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request, 'Error in address2 field')
        
        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in city field')

        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in state field')

        if 'zip' in request.POST: zip = request.POST['zip']
        else: messages.error(request, 'Error in zip field')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in email field')

        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username field')

        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in passord field')

        if 'agreecheck' in request.POST: agreecheck = request.POST['agreecheck']

        # Check The Values
        if fname and lname and address1 and address2 and city and state and zip and email and username and password:
            if agreecheck == 'on':
                # Check if username is taken 
                if User.objects.filter(username = username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    # Chich if email is taken 
                    if User.objects.filter(email = email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        # Create user
                        # user = User.objects.create_user( 
                        #     request.POST['username'],
                        #     request.POST['email'],
                        #     request.POST['password']
                        # )
                        user = User.objects.create_user(
                            first_name = fname,
                            last_name = lname,
                            email = email,
                            username = username,
                            password = password)
                        # Create userprofile
                        userProfile = UserProfile.objects.create(
                            user = user,
                            address1 = address1,
                            address2 = address2,
                            city = city,
                            state = state,
                            zip_number = zip
                        )
                        # Success create user
                        messages.success(request, 'Your account is created')
                        fname = ''
                        lname = ''
                        address1 = ''
                        address2 = ''
                        city = ''
                        state = ''
                        zip = ''
                        email = ''
                        username = ''
                        password = ''
                        agreecheck = None
                        is_added = True

            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'Check empty fields')
        
        context = {
            'fname': fname,
            'lname': lname,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'zip': zip,
            'email': email,
            'username': username,
            'password': password,
            'is_added': is_added
        }
        return render(request, 'accounts/signup.html', context)
    else:
        return render(request, 'accounts/signup.html', {})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')

def profile(request):
    if request.method == 'POST' and 'btnprofile' in request.POST:
        if request.user is not None:
            userprofile = UserProfile.objects.get(user = request.user)
            fname = request.POST['fname']
            lname = request.POST['lname']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            zip = request.POST['zip']
            password = request.POST['password']
            if fname and lname and address1 and address2 and city and state and zip and password:
                request.user.first_name = fname
                request.user.last_name = lname
                userprofile.address1 = address1
                userprofile.address2 = address2
                userprofile.city = city
                userprofile.state = state
                userprofile.zip_number = zip
                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                # save data
                request.user.save()
                userprofile.save()
                auth.login(request, request.user)
                # Success update user
                messages.success(request, 'Your data has been updated')
            else:
                messages.error(request, 'Check your values and elements')
        return redirect('profile')
    else:

        return render(request, 'accounts/profile.html', {})


def product_favorite(request, pro_id):
    pro_fav = Product.objects.get(pk=pro_id)
    if request.user.is_authenticated and not request.user.is_anonymous:
        if UserProfile.objects.filter(user=request.user, product_Favorite=pro_fav).exists():
            messages.success(request, 'Already product in the favorite list')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_Favorite.add(pro_fav)
            messages.success(request, 'Product has been favorited')
    else:
        messages.error(request, 'You must been logedd in')
    return redirect('/products/' + str(pro_id))


def show_product_favorite(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_Favorite.all()
    context = {'products': pro}
    return render(request, 'products/products.html', context)