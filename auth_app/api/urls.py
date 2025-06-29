from django.urls import path, include
from auth_app.api.views import RegistrationView, LoginView, RequestPassowrdResetView, VerifyTokenView, ResetPasswordView
from auth_app.functions import activate_user

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registerion'),
    path('login/', LoginView.as_view(), name='login'),
    path('resetPass/', RequestPassowrdResetView.as_view(), name='reset_password'),
    path('resetPass/<token>', ResetPasswordView.as_view(), name='reset_password_token'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate_user'),
    path('authorization/', VerifyTokenView.as_view(), name='authorization'),
]