from .models import StripeCustomer


class StripeSubscriptionEventHandler(object):
    """
    StripeEventHandler specifically handler subscription events
    """

    def __init__(self, event: dict) -> None:
        self.event = event

    def get_stripe_customer_id(self):
        return self.event["data"]["object"]["customer"]

    def process_event(self):
        # Handle the event
        # TODO: there could more scenarios we need to check

        stripe_customer_id = self.get_stripe_customer_id()
        if stripe_customer_id:
            if self.event["type"] in [
                "customer.subscription.created",
                "customer.subscription.deleted",
                "customer.subscription.updated",
            ]:
                StripeCustomer._activate_subscription(
                    stripe_customer_id, self.event["data"]["object"]
                )
