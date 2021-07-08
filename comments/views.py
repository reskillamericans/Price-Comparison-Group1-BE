from django.shortcuts import render, redirect
from .models import Comment
from products.models import Product

# Create your views here.

def index(request):
    shelf = Comment.objects.all()
    return render(request, 'comments.html', {'shelf' : shelf})

def post_detail(request, id):
    product = int(Product.objects.get(id=id))
    author = Comment.name (data=request.POST)
    comments = Comment.body(active=True)
    #create_comment = None

    #if product does not exist
    if product.is_valid():

        product.save()

    else:
        return redirect ('index')


    if request.method == 'POST':
        comment_form = Comment.body(data=request.POST)
        if comment_form.is_valid():

            create_comment = comment_form.save(commit=False)
            create_comment.save()
    else:
        comment_form = Comment.body()

    return render(request, 'comments.html', { 'product': product,
                            'author': author,
                            'comments' : comments,
                            'create_comment': create_comment})

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


