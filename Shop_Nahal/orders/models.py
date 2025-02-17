from django.db import models
from accounts.models import User
from products.models import Product
from django.core.validators import MinValueValidator,MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('paid','created')

    def __str__(self):
        return str(self.id)

    def get_total_not_discount(self):
        return sum(item.get_cost() for item in self.items.all() )

    def discount_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = int((self.discount / 100) * total)
            return discount_price
        return 0

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = int((self.discount / 100) * total)
            total = total - discount_price
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price


class Coupon(models.Model):
    code = models.CharField(max_length=30)
    from_valid = models.DateTimeField()
    to_valid = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)])

    def __str__(self):
        return self.code





