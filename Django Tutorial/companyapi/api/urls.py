from django.contrib import admin
from django.urls import path,include
from api.views import CompanyViewSet,EmpViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'companies',CompanyViewSet)
router.register(r'employees',EmpViewSet)

urlpatterns = [
    path('',include(router.urls))
]
 