from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,null=False,default="Rubi_food Category")
    description=models.TextField(max_length=255,null=False)
    category_image=models.ImageField(upload_to='media/',null=False)
    timestamp=models.DateTimeField(auto_now=False,default=timezone.now())# saved and set once
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural="Categories"

class Food(models.Model):
    food_name=models.CharField(max_length=25,null=False,default="Rubi_specials")
    food_description=models.TextField(max_length=200,null=False)
    quantity_available=models.IntegerField(null=False,default=0)
    unit_value=MoneyField(decimal_places=2,default_currency='KES',max_digits=6)
    food_image=models.ImageField(upload_to='media/',null=False)
    on_offer=models.BooleanField(null=False,default=False)
    belongs_to=models.ForeignKey(Category,on_delete=models.CASCADE)
    last_updated=models.DateTimeField(auto_now_add=False,auto_now=True)# updates when record is updated
    def __str__(self):
        return self.food_name
    def get_stock_count(self):
        return self.quantity_available
    # should only be executed by super admin
    def special_offer(self,discount):
        #if user is superadmin
        self.on_offer=True
        print(self.unit_value)
        self.unit_value=self.unit_value*( (100-discount)/100 )
        self.save()
        # if :# need to think about it
        #     print('BCIBivubIEWVBIEBIUECibvia')
        #     self.on_offer=False
        #     self.unit_value=(self.unit_value*100)/(100-discount)
        #     self.save()
        return self.unit_value
    def reduce_stock(self,qty):
        if self.quantity_available-qty<2:
            return "ERROR, Stock too Low"
        else:
            self.quantity_available-=qty
            self.save()
            return "SUCCESS, Stock updated"
    def update_stock(self,qty):
        self.quantity_available+=qty
        self.save()
        return "SUCCESS, Stock updated"

class Order(models.Model):
    ORD_No=models.CharField(max_length=255,null=False,default=datetime.datetime.now(),unique=True)
    foodid=models.ForeignKey(Food,on_delete=models.CASCADE,null=False,default=1)
    ordered_by=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    quantity = models.IntegerField(null=False, default=1)
    destination_addr=models.CharField(max_length=80,null=False,default='Nairobi CBD')
    status=models.CharField(max_length=20,default='PENDING',null=False)
    rating=models.FloatField(default=0.0,null=True)
    order_timestamp=models.DateTimeField(default=timezone.now()) #saved and set once
    #ord_amount=MoneyField(default_currency='KES',default=0.00,decimal_places=2)
    def get_order_amount(self): # no need to store calculated value
        Item = Food.objects.get(pk=self.foodid_id)
        amount=(self.quantity)*Item.unit_value
        return amount
    def rate_order(self,val):
        # quantize rating value
        val=val/50
        self.rating+=val
        if self.rating<10:
            self.save()
    def clear_order(self):
        self.status="CLEARED"
        self.save()
    def __str__(self):
        return self.ORD_No

class Cart(models.Model):
    cart_No=models.CharField(max_length=225,null=False)
    cart_status=models.CharField(max_length=20,null=False,default="PENDING")
    cart_timestamp=models.DateTimeField(default=timezone.now()) #saved and set once

    def __str__(self):
        return self.cart_No
    def get_cart_total(self): # this means the order table has to be populated first
        if self is None:
            total=0
        else:
            orders=str(self.cart_No)
            total=0
            delimited_orders=orders.split('#') # get all order numbers
            for order in delimited_orders:
                single_order=Order.objects.get(ORD_No=order) #find specific order obj
                print(single_order)
                total+=single_order.get_order_amount()# cummulatively sum the amount
        return total
    def clear_cart(self):
        if self is None:
            return None
        else:
            orders=str(self.cart_No)
            delimited_orders=orders.split('#') # get all order numbers
            for order in delimited_orders:
                single_order = Order.objects.get(ORD_No=order)  # find specific order obj
                single_order.clear_order()
            self.cart_status="CLEARED"
            self.save()

# for x in Order.objects.all():
#     print(x.get_order_amount())
# for item in Cart.objects.all():
#     print(item.get_cart_total())
