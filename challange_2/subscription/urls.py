from django.urls import path, re_path

from .views import index, my_subscription, subscription_products, checkout
from .webhook import handle_event

urlpatterns = [
    path("home", index, name="index"),
    path("my-subscription", my_subscription, name="my-subscriptions"),
    path(
        "subscription-products",
        subscription_products,
        name="subscription-products",
    ),
    re_path(
        r"^checkout/(?P<price_id>\w+)/?$", checkout, name="stripe-checkout"
    ),
    path("stripe-webhook", handle_event, name="stripe-webhooks"),
]
