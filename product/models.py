from django.db import models
from accounts.models import CustomUser
# Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
# 
#
# class Product(models.Model):
#
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#
#
#
#
# class Comment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     text = models.TextField()
#     rating = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user} - {self.product}'



