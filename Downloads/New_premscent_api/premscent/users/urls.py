from django.urls import path
from . import views
from .views import (
    RegisterView,
    LoginView,
    ServiceSeekerProfileView,
    ServiceProviderProfileView,
    ServiceCategoryListView,
    SubServiceListView,
    SpecificServiceListView,
    LogoutView,
    UserListView,
    ServiceProviderListView,
    UserDetailView,
    ServiceSeekerListView,
    ServiceSeekerDetailView, SpecificServiceDetailView,SubServiceDetailView,ServiceCategoryDetailView
)

app_name = 'users'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

       # Login Endpoint
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),  # Add the logout endpoint
    # Profile Update Endpoints
    path('profile/service-seeker/', ServiceSeekerProfileView.as_view(), name='service_seeker_profile'),
    path('profile/service-provider/', ServiceProviderProfileView.as_view(), name='service_provider_profile'),

    path('service-categories/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('service-category/<int:category_id>/sub-services/', SubServiceListView.as_view(), name='sub-service-list'),
    path('sub-service/<int:sub_service_id>/specific-services/', SpecificServiceListView.as_view(), name='specific-service-list'),


    path('service-categories/<int:pk>/', ServiceCategoryDetailView.as_view(), name='service-category-detail'),
    path('sub-services/<int:pk>/', SubServiceDetailView.as_view(), name='sub-service-detail'),
    path('specific-services/<int:pk>/', SpecificServiceDetailView.as_view(), name='specific-service-detail'),



    # for frontend test

    path('search/service-providers/', views.ServiceProviderSearchView.as_view(), name='service_provider_search'),



    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('service-providers/', ServiceProviderListView.as_view(), name='service-provider-list'),


    # Service seekers routes
    path('service-seekers/', ServiceSeekerListView.as_view(), name='service-seeker-list'),
    path('service-seekers/<int:pk>/', ServiceSeekerDetailView.as_view(), name='service-seeker-detail'),


    #search based on service category

]
