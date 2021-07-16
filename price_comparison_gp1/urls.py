from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from products.views import landing_page, about_us_view, contact_us_view

# from accounts.views import index

urlpatterns = [
                  # Admin pages
                  path('admin/', admin.site.urls),

                  # Homepage
                  path('', landing_page, name='index'),
                  path('contact_us', contact_us_view, name='contact_us'),
                  path('about_us', about_us_view, name='about_us'),

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
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name="registration/password_reset_form.html"),
                       name="password_reset_confirm"),
                  path('reset_password_complete/',
                       auth_views.PasswordResetCompleteView.as_view(
                           template_name="registration/password_reset_done.html"),
                       name="password_reset_complete"),
                  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
