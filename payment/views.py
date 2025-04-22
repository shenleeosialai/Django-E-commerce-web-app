from decimal import Decimal
import stripe
import json
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from orders.models import Order
from payment.mpesa.client import MpesaClient  # Make sure this is correctly implemented

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'stripe')

        if payment_method == 'stripe':
            success_url = request.build_absolute_uri(reverse('payment:completed'))
            cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }

            for item in order.items.all():
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                })

            if order.coupon:
                stripe_coupon = stripe.Coupon.create(
                    name=order.coupon.code,
                    percent_off=order.discount,
                    duration='once'
                )
                session_data['discounts'] = [{
                    'coupon': stripe_coupon.id
                }]

            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)

        elif payment_method == 'mpesa':
            phone_number = request.POST.get('phone')
            if not phone_number:
                messages.error(request, "Please provide your phone number for M-Pesa payment.")
                return redirect('payment:process')

            client = MpesaClient()
            amount = int(order.get_total_cost())

            response = client.stk_push(
                phone_number,
                amount,
                account_reference=str(order.id),
                transaction_desc="Order Payment"
            )

            if response and response.get("ResponseCode") == "0":
                return render(request, 'payment/mpesa_waiting.html', {'order': order})
            else:
                messages.error(request, "M-Pesa payment initiation failed. Please try again.")
                return redirect('payment:process')

    return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def mpesa_initiate(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        if not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)

        amount = int(order.get_total_cost())
        client = MpesaClient()

        response = client.stk_push(
            phone_number,
            amount,
            account_reference=str(order.id),
            transaction_desc="Order Payment"
        )

        if response and response.get("ResponseCode") == "0":
            return JsonResponse({'message': 'STK push sent. Please check your phone.'})
        else:
            return JsonResponse({'error': 'Failed to initiate payment'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    print("M-Pesa Callback received:", data)
    # You can process the data and update order status here
    return JsonResponse({"message": "Callback received"})
    # return HttpResponse(status=200)
