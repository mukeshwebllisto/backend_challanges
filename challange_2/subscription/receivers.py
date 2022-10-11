import stripe

from django.dispatch import receiver
from django.db import transaction
from django_registration.signals import user_registered
from django.contrib.auth import get_user_model
from django.conf import settings


from .stripe_client import StripeClient
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
    stripe_client = StripeClient()
    with transaction.atomic():
        stripe_customer_id = stripe_client.create_customer(user=user)

        StripeCustomer.objects.create(
            user=user, customer_id=stripe_customer_id
        )
