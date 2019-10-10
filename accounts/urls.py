from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import SignupUserViewSet

router = DefaultRouter()

router.register(r'signup', SignupUserViewSet)

urlpatterns = [
    path('login/', obtain_jwt_token),
    # since we live in a mutable stateful reality, we need some way to logout users authenticated via JWT
    # we can create tokens' blacklist, we can store tokens in DB and so on just to invalidate token
    # for simplicity, let's hope that nobody is able to steal tokens
    # also there is no need to add verifying logic in this app because there are no other communicating services
]

urlpatterns += router.urls
