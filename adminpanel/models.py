
from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast','Breakfast'),
        ('lunch','Lunch'),
        ('snacks','Snacks'),
        ('chocolates','Chocolates'),
        ('beverages','Beverages'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default="General")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adminpanel_orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Picked Up', 'Picked Up'),
        ('Paid', 'Paid'),
    ], default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_items(self):
        return self.orderitem_set.all()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"
    
    def calculate_total(self):
        total = sum(item.quantity * item.item.price for item in self.get_items())
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name} (Order #{self.order.id})"


class PaymentLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rs.{self.amount}  {self.method} payment   (Order #{self.order.id})"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
