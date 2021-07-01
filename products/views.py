import requests
from django.http import HttpResponse

def index(request):

    url = "https://amazon-products1.p.rapidapi.com/product"

    querystring = {"country":"US","asin":"B08BF4CZSV"}

    headers = {
        'x-rapidapi-key': "a071308572msh669a035361cc7f9p198a44jsnad143f87d6eb",
        'x-rapidapi-host': "amazon-products1.p.rapidapi.com"
        }


    response = requests.request("GET", url, headers=headers, params=querystring)


    return HttpResponse(response)


def index2(request):
    url = "https://ebay-com.p.rapidapi.com/product"

    querystring = {"URL":"https://www.ebay.com/itm/174807550468?hash=item28b3578a04:g:590AAOSwquxgR28h"}

    headers = {
        'x-rapidapi-key': "cd09594deamshbb8b2478ed8a011p1e756ajsnc0216f4bdfad",
        'x-rapidapi-host': "ebay-products.p.rapidapi.com"
        }

    response2 = requests.request("GET", url, headers=headers, params=querystring)

    return HttpResponse(response2)