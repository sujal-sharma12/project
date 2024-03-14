"""
URL configuration for AH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AH import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main,name="HomePage"),
    path('Login/', views.LoginPage,name="LoginPage"),
    path('Contact/', views.ContactPage,name="ContactPage"),
    path('About/', views.AboutPage,name="AboutPage"),
    path('Myaccount/', views.AccountPage,name="AccountPage"),
    path('Cart/', views.CartPage,name="CartPage"),
    path('Chekout/', views.CheckoutPage,name="ChekoutPage"),
    path('ChangePass/', views.ForgotPage,name="ChangePass"),
    path('Product/', views.PRODUCT,name="Productpage"),
    path('Details/<str:id>', views.DetailsPage,name="DetailsPage"),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
