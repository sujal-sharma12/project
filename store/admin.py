from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = images

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(images)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)
# Register your models here.

