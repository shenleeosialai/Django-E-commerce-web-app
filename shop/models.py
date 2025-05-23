from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    has_sizes = models.BooleanField(default=False)
    has_shoe_sizes = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Countdown(models.Model):
    title = models.CharField(max_length=100, default="Sale Ends In")
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.end_date}"


class NFTCard(models.Model):
    title = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='nft/images/')
    pdf = models.FileField(upload_to='nft/pdfs/')

    def __str__(self):
        return self.title
