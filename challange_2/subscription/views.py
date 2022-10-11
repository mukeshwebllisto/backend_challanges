import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .stripe_client import StripeClient

stripe.api_key = settings.STRIPE_SECRET_KEY

stripe_client = StripeClient()


def index(request):
    return render(request, "home.html")


def login(request):
    return render(request, "home.html")


@login_required
def my_subscription(request, *args, **kwargs):
    user = request.user
    context = {}
    try:
        subscription = stripe_client.get_subscriptions(user=user)
        context.update(
            {"is_subscribed": bool(subscription), "subscription": subscription}
        )
    except Exception as err:
        print(err, "err")
        context.update({"error": "Service Side Error"})
    return render(request, "my_subscriptions.html", context=context)


@login_required
def subscription_products(request, *args, **kwargs):
    context = {}
    try:
        context.update({"products": stripe_client.get_products()})
    except Exception as err:
        print(err, "err")
        context.update({"error": "Service Side Error"})
    return render(request, "subscription_products.html", context=context)


@login_required
def checkout(request, price_id, *args, **kwargs):
    context = {}
    if bool(stripe_client.get_subscriptions(user=request.user)):
        context.update(
            {
                "error": "A subscription already exists for customer. please visit customer portal page.",
                "products": stripe_client.get_products(),
            }
        )
        render(request, "subscription_products.html", context=context)
    else:
        try:
            stripe_checkout_url = stripe_client.get_checkout_page(
                user=request.user, price_id=price_id
            )
            return redirect(stripe_checkout_url)
        except Exception as err:
            print(err, "err")
            return redirect("my-subscription")
