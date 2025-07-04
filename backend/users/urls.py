from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    RegisterView,
    ProfileView,
    VerifyEmailView,
    GoogleAuthView,
    PasswordResetView,
    PasswordResetConfirmView,
    ResendVerificationView,
    UserSubscriptionView,
)
from .admin_views import AdminUserSubscriptionView  # Import the renamed admin view here

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Add an additional profile path without trailing slash for flexibility
    path('profile', ProfileView.as_view(), name='profile_no_slash'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('google/', GoogleAuthView.as_view(), name='google_auth'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend_verification'),
    path('subscription/', UserSubscriptionView.as_view(), name='user_subscription'),
    # Use the renamed admin view class
    path('admin/user-subscription/', AdminUserSubscriptionView.as_view(), name='admin_user_subscription'),
    path('api/get-subscription/', UserSubscriptionView.as_view(), name='get-subscription'),
]
