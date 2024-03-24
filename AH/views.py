from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from store.models import  Product,Categories,Filter_Price,Profile,contact_us
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def Main(request):
     product = Product.objects.filter(status='PUBLISH')

     context ={
         'product': product,
     }
     return render(request,'index.html', context)

def LoginPage(request):
    return render(request,'login.html')

def CartPage(request):
    return render(request,'cart.html')


def CheckoutPage(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    context = {'profile':profile}
    return render(request,'checkout.html',context)

def ContactPage(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        contact=contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        return redirect('/')
    return render(request,'contact.html')

def AboutPage(request):
    return render(request,'about.html')

def ForgotPage(request):
    return render(request,'forgot.html')

def registration(request):
    return render(request,'registrations.html')

def placeorder(request):
    return render(request,'placeorder.html')

def related(request):
    product = Product.objects.filter(status='PUBLISH')[:4]
    context ={
        'product': product,
    }
    return render(request,'related.html',context)

def PRODUCT(request):
    # product = Product.objects.filter(status='PUBLISH')
    categories=Categories.objects.all()
    filter_price=Filter_Price.objects.all()
    CATID=request.GET.get('categories')
    Filter_Price_id=request.GET.get('filter_price')

    if CATID:
        product=Product.objects.filter(categories=CATID,status='PUBLISH')
    elif Filter_Price_id:
        product=Product.objects.filter(filter_price=Filter_Price_id,status='PUBLISH')
    else:
        product=Product.objects.filter(status='PUBLISH')

    context ={
         'product': product,
         'categories':categories,
        #  'subcategories':subcategories,
         'filter_price':filter_price,
     }

    return render(request,'shop-left-sidebar.html',context)

def DetailsPage(request,id):
    prod=Product.objects.filter(id = id ).first()
    context={
         'prod': prod,
    }
    return render(request,'single-product.html',context)

def regstore(request):
    # auth_user
    myfname = request.POST['fname']
    mylname = request.POST['lname']
    myemail = request.POST['email']
    myusername = request.POST['username']
    mypassword = request.POST['password']
    mycpassword = request.POST['cpassword']
    mygender = request.POST['gender']  # Assuming you're using gender in the form
    mycontact = request.POST['contact']
    myaddress = request.POST['address']

    if mypassword == mycpassword:
        result = User.objects.create_user(first_name=myfname, last_name=mylname, email=myemail, username=myusername, password=mypassword)
        Profile.objects.create(gender=mygender,contact=mycontact, address=myaddress, user_id=result.id)
        return redirect('/Login/')
    else:
        messages.success(request, "Mismatch Password")
        return redirect('/registration/')
def login_check(request):
    myusername = request.POST.get('username')
    mypassword = request.POST.get('password')

    result = auth.authenticate(username=myusername,password=mypassword)
    if result is None:
	    messages.success(request, "Invalid Username or Password")
	    return redirect('/Login/')
    else:
        if result.is_superuser:
            messages.success(request, "Invalid Username or Password")
            return redirect('/Login/')
        else:
            auth.login(request, result)
            return redirect('/')
def logout(request):
    auth.logout(request)
    return redirect('/Login/')

def profile(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    context = {'profile':profile}
    return render(request,'profile.html',context)

def profile_edit(request,id):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    context = {'profile':profile}
    return render(request,'profile_edit.html',context)

def profile_update(request,id):
    # auth_user
    myfname = request.POST['fname']
    mylname = request.POST['lname']
    myemail = request.POST['email']
    myusername = request.POST['username']
    mygender = request.POST['gender']  # Assuming you're using gender in the form
    mycontact = request.POST['contact']
    myaddress = request.POST['address']

    data={
        'first_name':myfname,
        'last_name':mylname,
        'email':myemail,
        'username':myusername,
        'gender':mygender,
        'contact':mycontact,
        'address':myaddress
    }
    
    User.objects.update_or_create(pk=id,defaults=data)
    Profile.objects.update_or_create(user_id=id,defaults=data)

    return redirect('/profile')

def profile_address(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    context = {'profile':profile}
    return render(request,'profile_address.html',context)

def search(request):
    query=request.GET.get('query')
    context = {}
    return render(request,'search.html',context)

def update_password(request):
    if request.method == "POST":
        old_password = request.POST['pwd1']
        new_password = request.POST['pwd2']
        confirm_password = request.POST['pwd3']

        user = User.objects.get(username=request.user.username)

        # Check if the old password matches the current password
        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect("/update_password/")

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect("/update_password/")

        # Set and save the new password
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully.')
        return redirect("/Login/")

    return render(request, 'changepassword.html')
   


@login_required(login_url="/Login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")

@login_required(login_url="/Login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/Login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/Login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/Login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/Login/")
def cart_detail(request):
    return render(request, 'cart_details.html')
    

