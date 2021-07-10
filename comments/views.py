from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from products.models import Product

from .forms import *


# List all comments of current user
@login_required(login_url="accounts:login")
def index(request):
    comments_list = Comment.objects.filter(user=request.user)
    return render(request, 'comments/my_comments.html', {'comments_list': comments_list})


# def post_detail(request, id):
#     product = int(Product.objects.get(id=id))
#     author = Comment.name(data=request.POST)
#     comments = Comment.body(active=True)
#     # create_comment = None
#
#     # if product does not exist
#     if product.is_valid():
#         product.save()
#     else:
#         return redirect('index')
#
#     if request.method == 'POST':
#         comment_form = Comment.body(data=request.POST)
#         if comment_form.is_valid():
#             create_comment = comment_form.save(commit=False)
#             create_comment.save()
#     else:
#         comment_form = Comment.body()
#
#     return render(request, 'comments.html', {'product'       : product,
#                                              'author'        : author,
#                                              'comments'      : comments,
#                                              'create_comment': create_comment
#                                              })


# Create a comment
@login_required(login_url="accounts:login")
def create_comment(request, product_id):
    if request.method == 'POST':
        Comment.objects.create(user=request.user,
                               product=Product.objects.get(pk=product_id),
                               body=request.POST['comment_body'],
                               active=True)
    return redirect('products:product', pk=product_id)


# Edit a comment
@login_required(login_url="accounts:login")
def edit_comment(request, comment_id):
    # Try to get the comment
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if current user created the comment
    if request.user == comment.user:
        # Create form with comment info
        form = EditCommentForm(instance=comment)

        # Check if request was POST and button was "Update"
        if request.method == 'POST' and 'Update' in request.POST:
            # Create the form using POST data
            form = EditCommentForm(request.POST, instance=comment)

            # Verify form data is valid
            if form.is_valid():
                # Mark the comment as edited and save the edit date
                comment = form.save(commit=False)
                comment.edited = True
                comment.edited_on = timezone.now().strftime("%d %b %Y %I:%M %p")
                comment.save()
                messages.success(request, "Updated comment.")
                return redirect('products:product', pk=comment.product.pk)

        # If cancel was clicked, return to previous page
        elif request.method == 'POST' and 'Cancel' in request.POST:
            return redirect('products:product', pk=comment.product.pk)

        # Render the form with any bound data
        context = {'form': form, 'comment': comment}
        return render(request, 'comments/edit_comment.html', context)
    else:
        messages.error(request, f'You are not authorized to perform that action.')
        return redirect('comments:index')


# Delete comment
@login_required(login_url="accounts:login")
def delete_comment(request, comment_id):
    redirect_url = request.META["HTTP_REFERER"]
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if current user created the comment
    if request.user == comment.user:
        # Delete comment
        comment.delete()
        return redirect(redirect_url)
    else:
        messages.error(request, f'You are not authorized to perform that action.')
        return redirect(redirect_url)
