from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    image_url = models.URLField(null=True, default=None)

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    active = models.BooleanField()


class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=32)


class StripeCustomerSubscription(models.Model):
    customer = models.OneToOneField(StripeCustomer, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=64)
    stripe_subscription_id = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    cancel_at_period_end = models.BooleanField(default=False)
