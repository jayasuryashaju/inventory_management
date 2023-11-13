from django.db import models

# Create your models here.
class ScannedData(models.Model):
    barcode = models.CharField(max_length=255)
    other_column = models.CharField(max_length=255)
    marked_column = models.CharField(max_length=255, blank=True, null=True)

class Order(models.Model):
    tracking_number = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    weight = models.FloatField()

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"