from django.core.management.base import BaseCommand
from shop.models import Product
from shop.recommender import Recommender
import random


class Command(BaseCommand):
    help = 'Seed Redis with mock co-purchase data for recommendations'

    def handle(self, *args, **options):
        products = list(Product.objects.all())
        r = Recommender()

        # simulate co-purchases
        for _ in range(100):
            bought = random.sample(products, k=2)
            r.products_bought(bought)

        self.stdout.write(self.style.SUCCESS('Seeded recommendation data.'))
        
        
# To avoid the "no recommendations yet" issue before real sales happen, 
# i pre-seed Redis using dummy co-purchase data