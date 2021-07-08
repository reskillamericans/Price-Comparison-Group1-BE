from django.urls import path
from . import views

app_name= 'comments'

urlpatterns = [
    path('', views.index, name= 'index'),
    #path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('comments/', views.post_detail, name='comments'),
    path('edit/', views.update_comment, name= 'edit'),
    path('deleteComment/', views.delete_comment, name= 'delete')

]