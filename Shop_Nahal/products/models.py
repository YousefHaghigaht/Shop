from django.db import models
from accounts.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='scategory',blank=True,null=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        ordering = ('-is_sub',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to='%Y/%m/%d/')
    is_available = models.BooleanField(default=True)
    price = models.IntegerField()
    description = models.TextField()
    comments = GenericRelation(Comment)
    views = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def like_count(self):
        return self.pliked.count()


class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvots')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pliked')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - liked - {self.product}'


