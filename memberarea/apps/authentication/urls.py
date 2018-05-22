from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    UserRetrieveAPIView, UserListAPIView
)

urlpatterns = [
    path('/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/v', TokenVerifyView.as_view(), name='token_verify'),
    path('/token/r', TokenRefreshView.as_view(), name='token_refresh'),
    path('/current', UserRetrieveAPIView.as_view()),
    path('', UserListAPIView.as_view()),
]
