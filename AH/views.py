from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from store.models import  Product,Categories,Filter_Price,Profile,contact_us,Order,Orderitem,SubCategories
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
from django.views.decorators.csrf import csrf_exempt


def Main(request):
     product = Product.objects.filter(status='PUBLISH')[:8]
     context ={
         'product': product,
         }
     return render(request,'index.html', context)

def LoginPage(request):
    return render(request,'login.html')

def invoice_page(request):
    o_id=request.POST['o_id']
    order_obj=Order.objects.get(id=o_id)
    order_item=Orderitem.objects.filter(order_id=order_obj)
    customer_id = request.user.id
    customer_obj=User.objects.get(id=customer_id)
    profile_obj=Profile.objects.get(user_id=customer_obj)
    return render(request,"invoice.html",{'customer_obj':customer_obj,'profile_obj':profile_obj,'order_obj':order_obj,'order_item':order_item})

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
    if request.method == "POST":
        uid=request.user.id
        myuser=User.objects.get(id=uid)
        cart=request.session.get('cart')
        myfirstname=request.POST.get('firstname')
        mylastname =request.POST.get('lastname')
        mydob=request.POST.get('dob')
        mystate=request.POST.get('state')
        myaddress=request.POST.get('address')
        mycity=request.POST.get('city')
        mypincode=request.POST.get('pincode')
        myamount=request.POST.get('amount')
        myphone=request.POST.get('phone')
        myemail=request.POST.get('email')
        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')
        mypayment_method=request.POST.get('payment')
        order=Order.objects.create(user=myuser,firstname=myfirstname,lastname=mylastname,dateofbirth=mydob,state=mystate,address=myaddress,city=mycity,pincode=mypincode,amount=myamount,phone=myphone,email=myemail,payment_id=order_id,payment_method=mypayment_method)
        # order = Order.objects.get(user=myuser, id=order.id)
        for i in cart:
            a = float(cart[i]['price'])
            b=cart[i]['quantity']
            total=a*b
            item=Orderitem(
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total,
            )
            item.save()
            
    if mypayment_method == ' Cash On Delivery':
        return redirect('/thankyou/')
    else:
        return redirect('/payment_process/')
	
def thankyou(request):
    return render(request,'thank-you-page.html')

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
        #   'subcategories':subcategories,
         'filter_price':filter_price,
     }

    return render(request,'shop-left-sidebar.html',context)

def DetailsPage(request,id):
    prod=Product.objects.filter(id = id ).first()
    related = Product.objects.filter(categories=prod.categories).exclude(id=id)[:4]
    context={
         'prod': prod,
         'related': related,
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

def orderhistory(request):
    userid=request.user.id
    order=Order.objects.filter(user_id=userid)
    if not order:
        messages.success(request, "You have no orders yet.")
        return render(request,'orderhistory.html')
    else:
        message = ''
        context = {'order':order}
        return render(request,'orderhistory.html',context)

def orderview(request,id):
    orderitem  =Orderitem.objects.filter(order_id=id)
    order =Order.objects.get(id=id)
	
    context = {'orderitem':orderitem,
                'order':order,
    }
    return render(request,'orderview.html',context)

def payment_process(request):
    key_id = 'rzp_test_PvM4GxK9MYlCUc'
    key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'

    obj= Order.objects.filter(user_id=request.user.id).order_by('-id')[0]
    amount = float(obj.amount) * 100

    client = razorpay.Client(auth=(key_id, key_secret))

    data = {
        'amount': amount,
        'currency': 'INR',
        "receipt":"OIBP",
        "notes":{
            'name' : 'AK',
            'payment_for':'OIBP Test'
        }
    }
    id = request.user.id
    result = User.objects.get(pk=id)
    payment = client.order.create(data=data)
    context = {'payment' : payment,'result':result}
    return render(request, 'payment_process.html',context)

@csrf_exempt
def success(request):
    order = Order.objects.filter(user=request.user)
    latest_order = order.latest('id') 
    online_payment_done = True  
    latest_order.paid = online_payment_done
    latest_order.save()
    context = {}
    return render(request,'payment_success.html',context)

def search(request):
    query=request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product': product
    }
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
    

