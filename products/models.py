from django.db import models
from django.urls import reverse


class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='category')
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category' , args=[self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    image = models.ImageField()
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.is_available}'



