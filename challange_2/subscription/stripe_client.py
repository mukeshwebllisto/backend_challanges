import logging
import traceback

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import StripeCustomer

User = get_user_model()

logger = logging.getLogger(__name__)


class StripeClient:
    @property
    def __get_secret_key(self):
        return getattr(settings, "STRIPE_SECRET_KEY")

    def check_customer_exist(self, *, user: User) -> bool:

        try:
            stripe_customer = user.stripe_customer
        except StripeCustomer.DoesNotExist:
            raise ValueError("Stripe Customer Not exists")
        customer_obj = stripe.Customer.retrieve(
            stripe_customer.customer_id, api_key=self.__get_secret_key
        )

        return bool("deleted" in customer_obj)

    def create_customer(self, *, user: User) -> str:
        """
        create_customer function creates customer on stripe
        Args:
            user: User
        Returns:
            stripe_customer_id: str
        """
        stripe_customer = stripe.Customer.create(
            api_key=self.__get_secret_key,
            name=user.get_full_name(),
            email=user.email,
        )
        return stripe_customer["id"]

    def get_products(self):
        """
        funtion `get_products` will list down all the product associcate with given currency
        funtion will make
        1. API call to stripe to get all the prices
        2. make more api call to get the product details for each price_id
        """
        product_list = []
        has_more = True
        starting_after = None
        while has_more:
            resp = stripe.Price.list(
                api_key=self.__get_secret_key,
                active=True,
                starting_after=starting_after,
                expand=["data.product"],
            )
            product_list.extend(
                [
                    {
                        "price_id": price["id"],
                        "id": price["product"],
                        "amount": float(price["unit_amount"]) / 100,
                        "currency": price["currency"],
                        "price_name": price["metadata"].get(
                            "name", "Recurring"
                        ),
                        **price["product"],
                    }
                    for price in resp["data"]
                    if price["product"]["active"]
                ]
            )
            if resp["has_more"]:
                starting_after = resp["data"][-1]["id"]
                continue
            break

        return product_list

    def get_subscriptions(self, user: User):
        try:
            stripe_customer = user.stripe_customer
        except StripeCustomer.DoesNotExist:
            raise ValueError("Stripe Customer Not exists")

        return stripe.Subscription.list(
            api_key=self.__get_secret_key,
            limit=1,
            customer=stripe_customer.customer_id,
        )

    def get_checkout_page(self, user: User, price_id: str) -> str:
        """
        get_checkout_page function returns stripe checkout page url for
        the first subscription
        Args:
            user: User
            price_id: str
        Returns:
            url: stripe checkout session url
        """

        try:
            stripe_customer = user.stripe_customer
        except StripeCustomer.DoesNotExist:
            raise ValueError("Stripe Customer Not exists")

        price = stripe.Price.retrieve(
            api_key=self.__get_secret_key,
            id=price_id,
        )
        checkout_session = stripe.checkout.Session.create(
            api_key=self.__get_secret_key,
            customer=stripe_customer.customer_id,
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            allow_promotion_codes=True,
            payment_method_types=["card"],
            subscription_data={
                "trial_period_days": price.recurring.trial_period_days,
            },
            success_url=settings.STRIPE_CHECKOUT_SUCCESS_URL,
            cancel_url=settings.STRIPE_CHECKOUT_CANCEL_URL,
        )
        return checkout_session.url

    def get_customer_portal(self, user: User) -> str:
        """
        get_customer_portal function returns stripe customer portal page url for
        the already subscribed customers
        Args:
            user: User
        Returns:
            url: stripe customer portal url
        """

        try:
            stripe_customer = user.stripe_customer
        except StripeCustomer.DoesNotExist:
            raise ValueError("Stripe Customer Not exists")

        customer_portal_session = stripe.billing_portal.Session.create(
            api_key=self.__get_secret_key,
            customer=stripe_customer.customer_id,
            return_url=settings.STRIPE_CUSTOMER_PORTAL_RETURN_URL,
        )
        return customer_portal_session.url

    # def safe_cancel_substription_if_exists(self, restaurant: Restaurant, currency_code: str) -> list:
    #     owner = restaurant.owner
    #     try:
    #         list_subscription = self.get_subscriptions(restaurant=restaurant, currency_code=currency_code)
    #         if bool(list_subscription):
    #             [
    #                 stripe.Subscription.delete(subscription["id"], api_key=self.__get_secret_key(currency_code))
    #                 for subscription in list_subscription.get("data", [])
    #             ]

    #     except Exception as err:
    #         logger.error(f"{traceback.format_exc()} for user account : {owner.email} , restaurant : {restaurant.name}")

    # def delete_customer(self, restaurant: Restaurant, currency_code: str) -> bool:
    #     customer_deleted_status = stripe.Customer.delete(restaurant.stripe_customer_id, api_key=self.__get_secret_key(currency_code))
    #     return customer_deleted_status["deleted"]
