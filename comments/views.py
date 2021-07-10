from django.shortcuts import render, redirect
from .models import Comment
from products.models import Product

# Create your views here.

def index(request):
    products = Product.objects.all()
    shelf = Comment.objects.all()
    context = {
        'products' : products,
        'shelf' : shelf
    }
    return render(request, 'comments.html', context)


def post_detail(request, id):
    get_product = Product.objects.get(id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment')

        create_comment = Comment(body=comment, product=get_product, user=request.user)
        create_comment.save()
    
    

    return render(request, 'comments.html')

def update_comment(comment_id):
    try:
        comment_sel = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
        return redirect('index')
    
def delete_comment(comment_id):
    try:
        comment_sel = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
        return redirect('index')
    comment_sel.delete()
    return redirect('index')


