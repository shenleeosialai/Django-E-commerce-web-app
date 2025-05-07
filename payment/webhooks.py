import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed
import json
from django.http import JsonResponse


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
                    payload,
                    sig_header,
                    settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            # store Stripe payment ID
            order.stripe_id = session.payment_intent
            order.save()
            # launch asynchronous task
            payment_completed.delay(order.id)

    return HttpResponse(status=200)


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body.decode('utf-8'))
    stk_callback = data.get("Body", {}).get("stkCallback", {})

    if stk_callback.get("ResultCode") == 0:
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        phone = next((item["Value"] for item in metadata if item["Name"] == "PhoneNumber"), None)
        mpesa_code = next((item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)
        amount = next((item["Value"] for item in metadata if item["Name"] == "Amount"), None)

        # Find and update the order
        try:
            order = Order.objects.filter(email=request.GET.get("email")).last()  # customize as needed
            order.paid = True
            order.mpesa_code = mpesa_code
            order.save()
        except Order.DoesNotExist:
            pass

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
