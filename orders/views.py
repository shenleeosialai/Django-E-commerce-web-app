from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.payment_status = 'PENDING'
            order.status = 'processing'
            if request.user.is_authenticated:
                order.email = request.user.email


            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         size=item['size'])
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                  {'form': form})

def track_order(request):
    order = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        filters = Q(id=order_id, email=email)

        if date_from:
            filters &= Q(created__gte=parse_date(date_from))
        if date_to:
            filters &= Q(created__lte=parse_date(date_to))

        order = Order.objects.filter(filters).first()
        if not order:
            messages.error(request, "Order not found. Please check your details.")

    return render(request, 'orders/order/track.html', {'order': order})

@login_required
def order_history(request):
    # Assuming your Order model has a user or email field to link orders to users
    # If you link orders by email, you can filter by request.user.email
    # Adjust according to your Order model
    orders = Order.objects.filter(email=request.user.email).order_by('-created')
    return render(request, 'orders/order/history.html', {'orders': orders})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(OrderItem, order_id=order_id)
    return render(request, 'orders/order/created.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS
                                                        (settings.STATIC_ROOT /
                                                         'css/pdf.css')])
    return response
