"""price_comparison_gp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from products.views import ProductIndexView
# from accounts.views import index

urlpatterns = [
    # Homepage
    path('', ProductIndexView.as_view(), name='index'),

    # apps
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('comments/', include('comments.urls')),

    # Password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),

    # Admin site
    path('admin/', admin.site.urls)

    ]
