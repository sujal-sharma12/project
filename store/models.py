from django.db import models
from  django.utils import timezone
import datetime

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class SubCategories(models.Model):
    name = models.CharField(max_length=200)  # Add any additional fields you need
    # Add any other fields as per your requirements
    
    def __str__(self):
        return self.name
    
class Filter_Price(models.Model):
    FILTER_PRICE=(
        ('1000 to 10000','1000 to 10000'),
        ('10000 to 20000','10000 to 20000'),
        ('20000 to 30000','20000 to 30000'),
        ('30000 to 40000','30000 to 40000'),
        ('40000 to 50000','40000 to 50000'),
        ('More than 50000','More than 50000')
    )    
    Price = models.CharField(choices=FILTER_PRICE,max_length=60)
    def __str__(self):
        return self.Price     
    
class Product(models.Model):
    STATUS=(('PUBLISH','PUBLISH'),('DRAFT','DRAFT'))

    unique_id=models.CharField(unique=True, max_length=200,null=True,blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/',max_length=300,null=True,default=None)#uplod to=Product_images/img in video
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    status=models.CharField(choices=STATUS,max_length=200,default='PUBLISH')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE,default=2)
    subcategories = models.ForeignKey(SubCategories, on_delete=models.CASCADE,default=2)
    filter_price =models.ForeignKey(Filter_Price, on_delete=models.CASCADE,default=5)
    created_date = models.DateTimeField(default=timezone.now) 
    #def product_photo(self):
    #    return mark_safe('<img src="{}" width="100">'.format(self.image.url))

    def SAVE(self,*args,**kwargs):
        if not self.unique_id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name 
    
class images(models.Model):
    image=models.ImageField(upload_to='news/')        
    product=models.ForeignKey(Product, on_delete=models.CASCADE,default=1)