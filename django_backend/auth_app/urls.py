

from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    # path('auth/', auth_test_view, name='auth'),
]
