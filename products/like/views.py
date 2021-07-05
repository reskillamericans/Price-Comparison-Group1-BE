from django.shortcuts import render
from .models import LikeButton
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse

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
   return render(request,"like/like_template.html",ctx)