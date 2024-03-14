from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from store.models import  Product

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

def Productpage(request):
    return render(request,'shop-left-sidebar.html')