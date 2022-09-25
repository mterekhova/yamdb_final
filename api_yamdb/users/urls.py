from django.urls import include, path
from rest_framework import routers

from .views import APISignup, APIToken, UserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')


urlpatterns = [
    path('signup/', APISignup.as_view()),
    path('token/', APIToken.as_view()),
    path('', include(router.urls)),
]
