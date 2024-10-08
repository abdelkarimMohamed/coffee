from django.db import models
from datetime import datetime
from django.urls import reverse

# Create your models here.
class Product(models.Model):

    name=models.CharField(max_length=150)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    photo=models.ImageField(upload_to='photos/%y/%m/%d')
    is_active=models.BooleanField(default=True)
    publish_data=models.DateTimeField(default=datetime.now)    
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-publish_data']

    # def get_absolute_url(self):

    #     return reverse("products:product",args=[
    #         self.publish_data.year,
    #         self.publish_data.month,
    #         self.publish_data.day,
    #         self.name,
    #     ])