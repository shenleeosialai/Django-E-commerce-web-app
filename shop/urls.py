from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),  # Homepage with featured products
    path('products/', views.product_list, name='product_list'),  # Shop All
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/countdown/', views.countdown_data, name='countdown_data'),
]
