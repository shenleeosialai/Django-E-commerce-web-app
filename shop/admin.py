from django.contrib import admin
from .models import Category, Product
from .models import Countdown
from .models import NFTCard


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'featured']
    list_filter = ['featured']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'updated',
                    'has_sizes', 'has_shoe_sizes', 'featured')
    list_filter = ('available', 'created', 'updated', 'has_sizes',
                   'has_shoe_sizes', 'featured')
    list_editable = ('price', 'available', 'has_sizes', 'has_shoe_sizes',
                     'featured')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Countdown)

admin.site.register(NFTCard)
