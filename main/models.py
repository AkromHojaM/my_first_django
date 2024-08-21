from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class About_img(models.Model):
    image = models.ImageField(upload_to="about")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product_img(models.Model):
    image = models.ImageField(upload_to="pics")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ShoppinCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.product.name} from {self.user.name}'
