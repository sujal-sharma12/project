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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main,name="HomePage"),
    path('Login/', views.LoginPage,name="LoginPage"),
    path('Contact/', views.ContactPage,name="ContactPage"),
    path('About/', views.AboutPage,name="AboutPage"),
    path('Cart/', views.CartPage,name="CartPage"),
    path('Chekout/', views.CheckoutPage,name="ChekoutPage"),
    path('ChangePass/', views.ForgotPage,name="ChangePass"),
    path('Product/', views.PRODUCT,name="Productpage"),
    path('regstore/', views.regstore,name="regstore"),
    path('registration/', views.registration,name="registration"),
    path('login_check/', views.login_check,name="login_check"),
    path('logout/', views.logout,name="logout"),
    path('related/', views.related,name="related"),
    path('profile/', views.profile,name="profile"),
    path('profile_address/', views.profile_address,name="profile_address"),
    path('profile_edit/<int:id>', views.profile_edit,name="profile_edit"),
    path('profile_update/<int:id>', views.profile_update,name="profile_update"),
    path('update_password/', views.update_password,name="update_password"),
    path('placeorder/', views.placeorder,name="placeorder"),
    path('search/', views.search,name="search"),
    path('Details/<int:id>', views.DetailsPage,name="DetailsPage"),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart_deatail/',views.cart_detail,name='cart_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
