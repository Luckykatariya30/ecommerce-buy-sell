from django.contrib import admin
from ecommerce_app.models import Contect,Product, Order, OrderUpdate

# Register your models here.

@admin.register(Contect)
class ContectAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone_number','desc']
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_id','product_name','category','subcategory','price','desc','product_images']

    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','items_json','amount','name','email','address1','address2','city','state','zip_code','phone']

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ['update_id', 'order_id', 'update_desc','delivered', 'timestamp']