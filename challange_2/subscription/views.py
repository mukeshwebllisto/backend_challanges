import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, "home.html")


def login(request):
    return render(request, "home.html")


# @login_required
# def checkout(request):

#     try:
#         # check if has active subscription
#         if request.user.customer.membership:
#             return redirect('settings')
#     except Customer.DoesNotExist:
#         pass

#     if request.method == 'POST':
#         pass
#     else:
#         membership = 'monthly'
#         final_dollar = 10
#         membership_id = 'price_1HI7iKKPNZZN53LZEYa55mwX'
#         if request.method == 'GET' and 'membership' in request.GET:
#             if request.GET['membership'] == 'yearly':
#                 membership = 'yearly'
#                 membership_id = 'price_1HI7ikKPNZZN53LZQxjBkO1e'
#                 final_dollar = 100

#         # Create Strip Checkout
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             customer_email = request.user.email,
#             line_items=[{
#                 'price': membership_id,
#                 'quantity': 1,
#             }],
#             mode='subscription',
#             allow_promotion_codes=True,
#             success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url='http://127.0.0.1:8000/cancel',
#         )

#         return render(request, 'membership/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})
