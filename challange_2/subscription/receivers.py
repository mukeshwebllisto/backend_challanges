import stripe

from django.dispatch import receiver
from django.db import transaction
from django_registration.signals import user_registered
from django.contrib.auth import get_user_model
from django.conf import settings


from .models import StripeCustomer

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


@receiver(user_registered)
def create_stripe_customer(sender, **kwargs):
    """
    Create stripe subscription for newly
    registered user
    """
    user = kwargs["user"]
    with transaction.atomic():
        stripe_customer = stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
        )

        StripeCustomer.objects.create(
            user=user, customer_id=stripe_customer.id
        )
