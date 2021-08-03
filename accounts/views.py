import environ

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_text, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .decorators import unauthenticated_user
from .forms import RegisterForm, LoginForm, UserInfoForm
from .models import User
from .tokens import account_activation_token

app_name = "CompareX"

env = environ.Env(
        # set casting, default value
        SEND_EMAIL=(bool, False)
        )
# reading .env file
environ.Env.read_env()
# Send email or instant verification
send_email = env('SEND_EMAIL')


# Homepage/landing page
def index(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/index.html', context)


# Login - only unauthenticated users can see this page
@unauthenticated_user
def login_view(request):
    # Check if request was POST
    if request.method == 'POST':
        # Get username & password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Verify user is valid
        if user is not None:
            # Login user
            login(request, user)

            # redirect to Product List page:
            return redirect('products:index')
        else:
            # Display error message
            messages.error(request, "Invalid login. Please try again.")

    # Render login page with any bound data and error messages
    context = {'form': LoginForm()}
    return render(request, 'accounts/login.html', context)


# Register - only unauthenticated users can see this page
@unauthenticated_user
def register_view(request):
    # Create blank form
    form = RegisterForm()

    # Check if request was POST
    if request.method == 'POST':
        # Populate the form with POST data
        form = RegisterForm(request.POST)

        # Verify form data is valid
        if form.is_valid():
            # Deactivate user until email is verified
            user = form.save(commit=False)
            user.is_active = False
            user.email = user.email.casefold()

            # Save the User model
            user.save()

            # If send_email is true, an email will be sent,
            # and user must go to link to activate account.
            if send_email:
                # Create verification email
                current_site = get_current_site(request)
                subject = f"Activate your {app_name} Account"
                message = render_to_string('accounts/activation_email.html',
                                           {
                                               'user'  : user,
                                               'scheme': request.scheme,
                                               'domain': current_site.domain,
                                               'uid'   : urlsafe_base64_encode(smart_bytes(user.pk)),
                                               'token' : account_activation_token.make_token(user),
                                               })

                # Send email
                user.email_user(subject, message)

                # Redirect to login page
                messages.success(request, f'A verification email has been sent to {user.email}.')
                messages.success(request, f'Please verify your email to complete registration.')
                return redirect('accounts:login')

            # If send_email is False, the user will be activated automatically
            else:
                # Activate the user
                user.is_active = True
                user.save()
                # Login the user
                login(request, user)
                messages.success(request, f'Your account has been confirmed.')
                return redirect('index')

    # Render the form with any bound data
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# Activate user - idb64 and token are supplied by the url
@unauthenticated_user
def activate_view(request, uidb64, token):
    if request.method == 'GET':
        # Retrieve user using the uid
        try:
            uid = smart_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        # If user cannot be retrieved, catch the error
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as err:
            user = None
            print(f"User is none:\n{err}")

        # If user is found, verify the token
        if user is not None and account_activation_token.check_token(user, token):
            # Activate the user and log them in
            user.is_active = True
            user.save()

            # Create confirmation email
            current_site = get_current_site(request)
            subject = f"{app_name} Registration complete."
            message = render_to_string('accounts/confirmation_email.html',
                                       {
                                           'user'  : user,
                                           'app'   : app_name,
                                           'scheme': request.scheme,
                                           'domain': current_site.domain,
                                           })

            # Send email
            user.email_user(subject, message)

            # Login the user
            login(request, user)
            messages.success(request, f'Your account has been confirmed.')
            return redirect('index')

        # If user is not found, show error message
        else:
            messages.warning(request, 'The confirmation link was invalid, '
                                      'possibly because it has already been used.')
            return redirect('index')


# Logout
def logout_view(request):
    # Logout user and send to login page
    logout(request)
    messages.info(request, "Successfully logged out.")
    return redirect("accounts:login")


# User Info - must be logged in to access this page
@login_required(login_url="accounts:login")
def user_info_view(request):
    # Create form with current user info
    form = UserInfoForm(instance=request.user)

    # Check if request was POST
    if request.method == 'POST':
        # Create the form using POST data
        form = UserInfoForm(request.POST, instance=request.user)

        # Verify form data is valid
        if form.is_valid():
            # Save the updates and reload page with data
            form.save()
            messages.success(request, "Updated user info.")
            return redirect('accounts:user_info')

    # Render the form with any bound data
    context = {'form': form}
    return render(request, 'accounts/user_info.html', context)


# FAQ
def faq_html(request):
    return render(request, 'accounts/faq.html')


