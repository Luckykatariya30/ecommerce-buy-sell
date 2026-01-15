from django.db import models

# Create your models here.


class Contect(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.IntegerField()
    desc = models.TextField(max_length=500)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.FloatField(max_length=20, default=0)
    desc = models.CharField(max_length=400)
    product_images = models.ImageField(upload_to='product_image/images')
    
    def __str__(self):
        return self.product_name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.FloatField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address1 = models.CharField(max_length=111)
    address2 = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name
    
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.update_desc[0:7] + "..."