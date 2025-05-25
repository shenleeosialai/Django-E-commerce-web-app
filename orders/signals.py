from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Order
from shop.recommender import Recommender


@receiver(post_save, sender=Order)
def update_recommendations_on_order_save(sender, instance, created, **kwargs):
    # Only run after payment is marked complete
    if instance.paid:
        if created or not Order.objects.filter(pk=instance.pk, paid=False).exists():
            products = [item.product for item in instance.items.all()]
            if products:
                recommender = Recommender()
                recommender.products_bought(products)

@receiver(pre_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
    if instance.pk:  # Only for updates
        old_order = Order.objects.get(pk=instance.pk)
        if old_order.status != instance.status:
            send_mail(
                subject=f"Order #{instance.id} Status Update",
                message=f"Dear {instance.first_name},\n\n"
                        f"Your order status has changed to: {instance.get_status_display()}.\n"
                        f"Thank you for shopping with us!",
                from_email='admin@myshop.com',
                recipient_list=[instance.email],
                fail_silently=True,
            )