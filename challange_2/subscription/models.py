import logging

from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from stripe.api_resources.subscription import Subscription


logger = logging.getLogger(__name__)

User = get_user_model()


class StripeCustomer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="stripe_customer"
    )
    customer_id = models.CharField(max_length=32)

    @classmethod
    def _handle_subscription(
        cls, stripe_customer_id: str, stripe_event: Subscription
    ) -> None:
        try:
            stripe_customer = cls.objects.get(customer_id=stripe_customer_id)
            StripeCustomerSubscription.objects.update_or_create(
                customer=stripe_customer,
                defaults={
                    "stripe_subscription_id": stripe_event.id,
                    "status": stripe_event.status,
                    "cancel_at_period_end": datetime.fromtimestamp(
                        stripe_event.current_period_end
                    ),
                },
            )
        except cls.DoesNotExist as err:
            logger.error(
                f"error : {err} | while handling stripe subscription event"
            )
            # different env issues, some customer may not exists in relative env
            return


class StripeCustomerSubscription(models.Model):
    customer = models.OneToOneField(StripeCustomer, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    cancel_at_period_end = models.BooleanField(default=False)
