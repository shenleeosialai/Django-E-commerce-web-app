from django.core.management.base import BaseCommand
from shop.models import Product
from shop.recommender import Recommender
import random

class Command(BaseCommand):
    help = 'Seed Redis with fallback recommendation data for all products'

    def handle(self, *args, **options):
        products = list(Product.objects.all())
        r = Recommender()

        # Simulate some global co-purchases to give base coverage
        for _ in range(100):
            bought = random.sample(products, k=2)
            r.products_bought(bought)

        # Ensure each product has at least N recommendations
        MIN_RECOMMENDATIONS = 4
        for product in products:
            current_recommendations = r.suggest_products_for([product], max_results=MIN_RECOMMENDATIONS)
            if len(current_recommendations) < MIN_RECOMMENDATIONS:
                # Try to find alternatives in the same category (if applicable)
                if hasattr(product, 'category'):
                    similar = Product.objects.filter(category=product.category).exclude(id=product.id)
                else:
                    similar = Product.objects.exclude(id=product.id)

                similar = list(similar)
                fallback = random.sample(similar, min(len(similar), MIN_RECOMMENDATIONS))

                # Simulate the user buying product + fallback
                r.products_bought([product] + fallback)

        self.stdout.write(self.style.SUCCESS('Seeded recommendation data with guaranteed minimum per product.'))



# To avoid the "no recommendations yet" issue before real sales happen,
# i pre-seed Redis using dummy co-purchase data
# docker-compose exec web python manage.py seed_recommendations