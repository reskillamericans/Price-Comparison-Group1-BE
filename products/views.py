import json

import requests
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

from .models import *

# Like icon details
like_icon = {'icon_name'    : 'fa-thumbs-up',
             'icon_size'    : '40px',
             'liked_color'  : "blue",
             'unliked_color': "lightgrey"
             }


# Show list of products
class ProductIndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.order_by('name')


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
    context = {'liked_products_list': liked_product_list}
    return render(request, 'products/liked_products.html', context)


# Saved Products - must be logged in to access this page
@login_required(login_url="accounts:login")
def saved_products_view(request):
    user = request.user
    saved_product_list = SavedProduct.objects.filter(user=user)
    context = {'saved_products_list': saved_product_list}
    return render(request, 'products/saved_products.html', context)


def amazon_view(request):
    url = "https://amazon-products1.p.rapidapi.com/product"
    querystring = {"country": "US", "asin": "B08BF4CZSV"}
    headers = {
        'x-rapidapi-key' : "a071308572msh669a035361cc7f9p198a44jsnad143f87d6eb",
        'x-rapidapi-host': "amazon-products1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    return HttpResponse(response)


def ebay_view(request):
    url = "https://ebay-com.p.rapidapi.com/product"
    querystring = {"URL": "https://www.ebay.com/itm/174807550468?hash=item28b3578a04:g:590AAOSwquxgR28h"}
    headers = {
        'x-rapidapi-key' : "cd09594deamshbb8b2478ed8a011p1e756ajsnc0216f4bdfad",
        'x-rapidapi-host': "ebay-products.p.rapidapi.com"
        }
    response2 = requests.request("GET", url, headers=headers, params=querystring)

    return HttpResponse(response2)
