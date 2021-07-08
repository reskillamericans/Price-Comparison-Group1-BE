import json
import requests
from django.shortcuts import render
from django.shortcuts import get_object_or_404 
from django.http import JsonResponse, HttpResponse
from .models import LikeButton, Product


def amazon(request):

    url = "https://amazon-products1.p.rapidapi.com/product"

    querystring = {"country":"US","asin":"B08BF4CZSV"}

    headers = {
        'x-rapidapi-key': "a071308572msh669a035361cc7f9p198a44jsnad143f87d6eb",
        'x-rapidapi-host': "amazon-products1.p.rapidapi.com"
        }


    response = requests.request("GET", url, headers=headers, params=querystring)
    resp = response.json()

    return JsonResponse(resp, safe=False)


def ebay(request):
    url = "https://ebay-com.p.rapidapi.com/product"

    querystring = {
        "URL" : "https://www.ebay.com/itm/174807550468?hash=item28b3578a04:g:590AAOSwquxgR28h"
    }

    headers = {
        'x-rapidapi-key': "cd09594deamshbb8b2478ed8a011p1e756ajsnc0216f4bdfad",
        'x-rapidapi-host': "ebay-products.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    resp = response.json()  

    return JsonResponse(resp, safe=False)


def like_button(request):
   if request.method =="POST":
       if request.POST.get("operation") == "like_submit" and request.is_ajax():
         content_id=request.POST.get("content_id",None)
         content=get_object_or_404(LikeButton,pk=content_id)
         if content.likes.filter(id=request.user.id): #already liked the content
            content.likes.remove(request.user) #remove user from likes 
            liked=False
         else:
             content.likes.add(request.user) 
             liked=True
         ctx={"likes_count":content.total_likes,"liked":liked,"content_id":content_id}
         return HttpResponse(json.dumps(ctx), content_type='application/json')

   contents=LikeButton.objects.all()
   already_liked=[]
   id=request.user.id
   for content in contents:
       if(content.likes.filter(id=id).exists()):
        already_liked.append(content.id)
   ctx={"contents":contents,"already_liked":already_liked}
   return render(request,"products/like_template.html",ctx)