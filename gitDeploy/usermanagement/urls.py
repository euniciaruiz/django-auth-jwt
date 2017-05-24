from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import AccountViewSet
from rest_framework import routers 


urlpatterns = [
    url(r'^login/', obtain_jwt_token),
    url(r'^accounts/', AccountViewSet),
]