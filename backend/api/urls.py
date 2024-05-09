# urls.py
from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', include(router.urls)), 
    path('get-csrf-token/', views.get_csrf_token, name="get-csrf-token"),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('airtime/', AirtimeListCreateView.as_view(), name='airtime-list-create'),
    path('data-api/', views.data_api, name='data_api'),
    path('vtu-api/', views.vtu_api, name='vtu_api'),
    path('data-plans/', views.data_plans, name='data_plans'),
    path('buy-data/', views.buy_data, name='buy_data'),
    path('sme-plans/', views.sme_plans, name='sme_plans'),
    path('buy-sme-data/', views.buy_sme_data, name='buy_sme_data'),
    path('phcn-plans/', views.phcn_plans, name='phcn_plans'),
    path('buy-phcn/', views.buy_phcn, name='buy_phcn'),
    path('tv-plans/', views.tv_plans, name='tv_plans'),
    path('buy-tv/', views.buy_tv, name='buy_tv'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/', get_user_details, name='get_user_details'),
     path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
]