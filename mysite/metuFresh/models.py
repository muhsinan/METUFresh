from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()

    class Meta:
        db_table = 'Product'

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default="123456")
    phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        db_table = 'Customer'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Order'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Order_Detail'


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default="123456")

    class Meta:
        db_table = 'Restaurant'

    def __str__(self):
        return str(self.name)


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    last_restocked_date = models.DateField()

    class Meta:
        db_table = 'Inventory'

    def __str__(self):
        return f"{self.product.name} - Stock: {self.stock_quantity}"
