from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from cart.forms import CartAddProductForm
from .models import Category, Product, Countdown, NFTCard
from .recommender import Recommender


# Homepage View (shows featured products, sections, NFTs)
def home(request):
    categories = Category.objects.all()

    # All globally featured products (marked as featured=True)
    global_featured_products = Product.objects.filter(featured=True,
                                                      available=True)[:6]

    # Category-specific featured sections
    featured_sections = []
    featured_categories = Category.objects.filter(featured=True)
    for c in featured_categories:
        featured_products = Product.objects.filter(category=c,
                                                   available=True)[:6]
        if featured_products:
            featured_sections.append({
                'category': c,
                'products': featured_products
            })

    # NFT cards for homepage
    nfts = NFTCard.objects.all()

    return render(request, 'shop/product/home.html', {
        'categories': categories,
        'featured_sections': featured_sections,
        'featured_products': global_featured_products,
        'nfts': nfts,
    })


# Product List View (used for "Shop All" and category-based browsing)
def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None

    # Category filter from URL
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Additional filters from GET parameters
    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'shop/product/category.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    })


# Product Detail View
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(product=product)
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 8)

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products
    })


# Countdown JSON API
def countdown_data(request):
    countdown = Countdown.objects.last()
    return JsonResponse({
        'title': countdown.title,
        'end_date': countdown.end_date.isoformat()
    })


# View NFT PDF
def view_pdf(request, nft_id):
    nft = get_object_or_404(NFTCard, id=nft_id)
    response = HttpResponse(nft.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline;filename=nft-art.pdf'
    return response
