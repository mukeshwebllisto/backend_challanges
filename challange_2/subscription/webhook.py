import stripe

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.views import View

from .services import StripeSubscriptionEventHandler


@csrf_exempt
def handle_event(request, *args, **kwargs):
    event = None
    payload = request.body
    sig_header = request.headers["STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    StripeSubscriptionEventHandler(event=event).process_event()
    return JsonResponse({"status": True})
