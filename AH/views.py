from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from store.models import  Product,Categories,Filter_Price

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
    return render(request,'checkout.html')

def ContactPage(request):
    return render(request,'contact.html')

def AboutPage(request):
    return render(request,'about.html')

def AccountPage(request):
    return render(request,'my-account.html')

def ForgotPage(request):
    return render(request,'forgot.html')

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