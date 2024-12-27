from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from accounts.views import RegisterAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
