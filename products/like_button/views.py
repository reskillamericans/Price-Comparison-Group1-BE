from django.shortcuts import render

# Create your views here.

def like_button(request):
    ctx={"hello":"hello"}
    return render(request, "like/like_template.html", ctx)