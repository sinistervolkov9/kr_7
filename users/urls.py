from django.urls import path
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', UserLogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    # path('register/', RegisterUserView.as_view(), name='register'),
    # path('verify/', VerifyUserView.as_view(), name='verify'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
