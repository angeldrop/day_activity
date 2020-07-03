from django.db import models

# Create your models here.

class DayActivityUserList(models.Model):
    id=models.TextField(default='',primary_key=True )
    order_number=models.TextField(default='')
    brach_type=models.TextField(default='')
    full_name=models.TextField(default='')
    

class Item(models.Model):
    text=models.TextField(default='')
    record_date_time=models.DateTimeField(auto_now=True)
    activity_date=models.DateField(auto_now=True)
    list=models.ForeignKey(DayActivityUserList,default=None,on_delete=models.CASCADE)
