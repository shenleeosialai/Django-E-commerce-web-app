from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from shop.recommender import Recommender


@receiver(post_save, sender=Order)
def update_recommendations_on_order_save(sender, instance, created, **kwargs):
    # Only run after payment is marked complete
    if instance.paid:
        products = [item.product for item in instance.items.all()]
        if products:
            recommender = Recommender()
            recommender.products_bought(products)
