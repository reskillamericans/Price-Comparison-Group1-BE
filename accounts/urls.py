from django.urls import path

from . import views
from .views import *

app_name = 'accounts'
urlpatterns = [
    # Homepage
    path('', index, name='index'),

    # Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>', activate_view, name='activate'),
    path('logout/', logout_view, name='logout'),

    # User info
    path('user_info/', views.user_info_view, name='user_info'),
    ]
