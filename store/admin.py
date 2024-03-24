from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = images

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'gender', 'contact', 'address')
    search_fields=['username']
    def gender(self, obj):
        return obj.profile.gender

    def contact(self, obj):
        return obj.profile.contact

    def address(self, obj):
        return obj.profile.address

class OrderitemTubleinline(admin.TabularInline):
    model = Orderitem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderitemTubleinline]



admin.site.register(images)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(contact_us)
admin.site.register(Order,OrderAdmin)
# Register your models here.

