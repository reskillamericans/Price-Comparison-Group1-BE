import decimal
import json

import cloudinary
import cloudinary.uploader
import environ
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from accounts.decorators import superuser_only, unauthenticated_user
from comments.models import Comment, Message
from test_files import ebay_products, amazon_products
from .forms import AddProductForm, ContactUsForm
from .models import Product, LikeButton, SavedProduct

env = environ.Env(
        # set casting, default value
        DEBUG_GP=(bool, False)
        )
environ.Env.read_env()

# Debug product fetching
debug_gp = env('DEBUG_GP')
amazon_responses = amazon_products.amazon_responses
ebay_responses = ebay_products.ebay_responses

# Like icon details
like_icon = {'icon_name'    : 'fa-heart',
             'icon_size'    : '60px',
             'liked_color'  : "gold",
             'unliked_color': "lightgrey"
             }


def landing_page(request):
    return render(request, 'products/landing_page.html')


def contact_us_view(request):
    form = ContactUsForm

    # Check if request was POST
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save message
            Message.objects.create(email=email, message=message)
            messages.success(request, f"Thank you for contacting us! "
                                      f"We will send a response to {email} "
                                      f"within 1-2 business days.")
            form = ContactUsForm

    # Render page with any bound data and error messages
    context = {'form': form}
    return render(request, 'products/contact_us.html', context)


def about_us_view(request):
    return render(request, 'products/about_us.html')


def modal_view(request):
    return render(request, 'products/product_modal.html')


# Show list of products
class ProductIndexView(generic.ListView):
    template_name = 'products/product_index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(ProductIndexView, self).get_context_data(**kwargs)

        # Price comparisons
        products = self.get_queryset()
        for product in products:
            product = get_savings(product)
        context['product_list'] = products
        return context


# Show product details
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['comments_list'] = Comment.objects.filter(product_id=pk)
        context['likes_list'] = LikeButton.objects.filter(product_id=pk)
        context['like_icon'] = like_icon
        user = self.request.user
        if user.is_authenticated:
            context['user_like'] = LikeButton.objects.filter(user=self.request.user, product_id=pk)
        else:
            context['user_like'] = False

        # Price comparisons
        product = self.object
        product = get_savings(product)
        # Stars
        product.star_list = get_stars(product.stars)
        context['product'] = product

        # Split description into list of lines
        description = product.description.splitlines()
        context['list_lines'] = description
        return context


class ModalDetail(generic.DetailView):
    model = Product
    template_name = 'products/modal.html'

    def get_context_data(self, **kwargs):
        context = super(ModalDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['likes_list'] = LikeButton.objects.filter(product_id=pk)

        # Price comparisons
        product = self.object
        product = get_savings(product)

        # Stars
        product.star_list = get_stars(product.stars)
        context['product'] = product
        return context


# Like button
def like_button(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            likes_id = request.POST.get("likes_id", None)
            like_object = get_object_or_404(LikeButton, pk=likes_id)

            # Check if user already liked product
            if like_object.user.filter(id=request.user.id):
                # Remove user like from product
                like_object.user.remove(request.user)
                liked = False
            else:
                # Add user like to product
                like_object.user.add(request.user)
                liked = True

            # Create new context to feed back to AJAX call
            context = {"likes_count": like_object.total_likes,
                       "user_like"  : liked,
                       "likes_id"   : likes_id
                       }
            return HttpResponse(json.dumps(context), content_type='application/json')


# Liked Products - must be logged in to access this page
@login_required(login_url="accounts:login")
def liked_products_view(request):
    user = request.user
    liked_product_list = LikeButton.objects.filter(user=user)
    for item in liked_product_list:
        item.product = get_savings(item.product)
    context = {'liked_product_list': liked_product_list}
    return render(request, 'products/liked_products.html', context)


# Saved Products - must be logged in to access this page
@login_required(login_url="accounts:login")
def saved_products_view(request):
    user = request.user
    saved_product_list = SavedProduct.objects.filter(user=user)
    context = {'saved_products_list': saved_product_list}
    return render(request, 'products/saved_products.html', context)


# Add Product - must be superuser
@superuser_only
def add_product_view(request):
    # Check if request was POST
    if request.method == 'POST':
        # Get amazon_asin & ebay_url
        amazon_asin = request.POST.get('amazon_asin')
        ebay_url = request.POST.get('ebay_url')

        # Create product
        product, error = create_product(amazon_asin, ebay_url)

        if product:
            messages.success(request, f"\"{product.name}\" has been created.")
        else:
            messages.error(request, f"Error: {error}")

    # Render page with any bound data and error messages
    context = {'form': AddProductForm()}
    return render(request, 'products/add_product.html', context)


# Edit Product View - must be superuser
@superuser_only
def edit_product_view(request):
    products_list = Product.objects.order_by('name')
    context = {'product_list': products_list}
    return render(request, 'products/edit_product.html', context)


# Update Product - must be superuser
@superuser_only
def update_product(request, product_id):
    # Retrieve product
    product = get_object_or_404(Product, pk=product_id)

    # Update product
    product, error = get_update(product)

    if product:
        messages.success(request, f"\"{product.name}\" has been updated.")
    else:
        messages.error(request, f"Error: {error}")
    return redirect('products:edit_product')


# Update Product - must be superuser
@superuser_only
def update_all_products(request):
    # Retrieve product
    product_list = Product.objects.all()

    for product in product_list:
        # Update product
        product, created = get_update(product)

        if product:
            messages.success(request, f"\"{product.name}\" has been updated.")
        else:
            messages.error(request, f"Error: {created}")

    return redirect('products:edit_product')


# Delete Product - must be superuser
@superuser_only
def delete_product(request, product_id):
    # Retrieve product
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name

    # Delete product
    product.delete()
    messages.success(request, f"\"{product_name}\" has been deleted.")
    return redirect('products:edit_product')


# Get amazon product from asin
def get_amazon_product(amazon_asin):
    url = env('AMAZON_URL')
    querystring = {"country": "US", "asin": amazon_asin}
    headers = {'x-rapidapi-key' : env('AMAZON_KEY'),
               'x-rapidapi-host': env('AMAZON_HOST')}

    if debug_gp:
        response = amazon_responses[int(amazon_asin)]
    else:
        response = requests.request("GET", url, headers=headers, params=querystring).json()

    amazon_context = {
        'asin'       : response['asin'],
        'price'      : response['prices']['current_price'],
        'description': response['description'],
        'image_urls' : response['images'],
        'url'        : response['full_link'],
        'stars'      : response['reviews']['stars'],
        }
    return amazon_context


# Get ebay product from url
def get_ebay_product(ebay_url):
    url = env('EBAY_URL')
    querystring = {"URL": ebay_url}
    headers = {'x-rapidapi-key' : env('EBAY_KEY'),
               'x-rapidapi-host': env('EBAY_HOST')}

    if debug_gp:
        response = ebay_responses[int(ebay_url)]
    else:
        response = requests.request("GET", url, headers=headers, params=querystring).json()

    ebay_context = {
        'name'      : response['title'],
        'price'     : response['prices']['current_price'],
        'url'       : response['full_link'],
        'image_urls': response['images'],
        }
    return ebay_context


# Get or crete product
def create_product(amazon_asin, ebay_url):
    # Get respective data
    amazon_product = get_amazon_product(amazon_asin)
    ebay_product = get_ebay_product(ebay_url)

    # Create a product
    try:
        product = Product.objects.create(
                amazon_asin=amazon_product['asin'],
                name=ebay_product['name'],
                description=amazon_product['description'],
                amazon_price=amazon_product['price'],
                ebay_price=ebay_product['price'],
                amazon_url=amazon_product['url'],
                ebay_url=ebay_product['url'],
                stars=amazon_product['stars'],
                )

        set_image(product, amazon_product['image_urls'] + ebay_product['image_urls'])

        # Return product, created
        return product, ""
    except ValidationError as e:
        return False, f"ValidationError:{e}"
    except LookupError as e:
        return False, f"LookupError:{e}"


# Get savings information
def get_savings(product: Product) -> Product:
    ap = product.amazon_price
    ep = product.ebay_price
    saver = "Amazon"
    if ep > ap > 0:
        savings = float(ep) - float(ap)
        percent = savings / float(ep) * 100
    elif ap > ep > 0:
        savings = float(ap) - float(ep)
        percent = savings / float(ap) * 100
        saver = "E-bay"
    elif ap == ep:
        savings = 0
        percent = 0
        saver = "either store"
    else:
        savings = 0
        percent = 0
        saver = "?"

    product.saver = saver
    product.savings = f"{savings:.2f}"
    product.percent = f"{percent:.0f}"
    return product


# Create star list
def get_stars(rating: decimal) -> list:
    whole_stars, half_stars = rating.as_tuple()[1]
    no_stars = rating.as_tuple()[0]
    stars = []
    if no_stars:
        stars = [0, 0, 0, 0, 0]
    else:
        for x in range(0, whole_stars):
            stars.append(1)
        if half_stars >= 5:
            stars.append(2)
        while len(stars) < 5:
            stars.append(0)
    return stars


def get_update(product: Product):
    # Get product info
    amazon_product = get_amazon_product(product.amazon_asin)
    ebay_product = get_ebay_product(product.ebay_url)

    # Create a product
    try:
        product.amazon_asin = amazon_product['asin']
        product.name = ebay_product['name']
        product.description = amazon_product['description']
        product.amazon_price = amazon_product['price']
        product.ebay_price = ebay_product['price']
        product.amazon_url = amazon_product['url']
        product.ebay_url = ebay_product['url']
        product.stars = amazon_product['stars']

        set_image(product, amazon_product['image_urls'] + ebay_product['image_urls'])

        # Return product, created
        return product, ""
    except ValidationError as e:
        return False, f"ValidationError:{e}"
    except LookupError as e:
        return False, f"LookupError:{e}"


def set_image(product: Product, image_urls):
    # Try to find a valid image url
    image_url = None
    for image in image_urls:
        if image:
            image_url = image
            break

    if image_url is not None:
        # Save image on Cloudinary
        image_response = cloudinary.uploader.upload(
                image_url,
                folder="products/",
                public_id=f"product_{product.pk}",
                overwrite=True,
                unique_filename=True,
                )
        product.image_url = image_url
        product.image = f"v{image_response['version']}/products/product_{product.pk}.{image_response['format']}"

    else:
        # image_file = '/products/image_not_found.png'
        # product.image = image_file
        product.image_url = staticfiles_storage.url("/images/products/image_not_found.png")

    # Save product
    product.save()
