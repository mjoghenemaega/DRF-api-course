from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from geopy.distance import geodesic
from drf_spectacular.utils import extend_schema
from django.shortcuts import render
from .permissions import AllowServiceSeekersAndUnauthenticated
from .models import ServiceProviderProfile, ServiceSeekerProfile
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    ServiceProviderProfileSerializer,
    ServiceSeekerProfileSerializer,
    LogoutResponseSerializer,
    UserSerializer
)
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model





def service_selection(request):
    return render(request, 'service_selection.html')  # Name of your HTML file

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import get_user_model
User = get_user_model()
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Query the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Use username for authentication
            user = authenticate(request, username=user.username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                # Redirect URL based on user role
                redirect_url = (
                    "/api/v1/profile/service-seeker/"
                    if user.role == 'seeker'
                    else "/api/v1/profile/service-provider/"
                )

                return Response(
                    {"token": token.key, "redirect_url": redirect_url},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Service Provider Profile View
class ServiceProviderProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceProviderProfileSerializer

    def get(self, request):
        try:
            profile = ServiceProviderProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServiceProviderProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response(self.serializer_class(profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        try:
            profile = ServiceProviderProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ServiceProviderProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


# Service Seeker Profile View
class ServiceSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSeekerProfileSerializer
    def get(self, request):
        try:
            profile = ServiceSeekerProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServiceSeekerProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response(self.serializer_class(profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = ServiceSeekerProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ServiceSeekerProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)





from rest_framework import generics
from .models import ServiceCategory, SubService, SpecificService
from .serializers import ServiceCategorySerializer, SubServiceSerializer, SpecificServiceSerializer


# View for fetching all service categories
class ServiceCategoryListView(generics.ListAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()  # Custom creation logic if needed


# View for fetching sub-services within a specific category
class SubServiceListView(generics.ListAPIView):
    serializer_class = SubServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SubService.objects.filter(category_id=category_id)


    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        category = ServiceCategory.objects.get(id=category_id)
        serializer.save(category=category)  # Ensure the sub-service is linked to the correct category



# View for fetching specific services within a specific sub-service
class SpecificServiceListView(generics.ListAPIView):
    serializer_class = SpecificServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        sub_service_id = self.kwargs['sub_service_id']
        return SpecificService.objects.filter(sub_service_id=sub_service_id)

    def perform_create(self, serializer):
        sub_service_id = self.kwargs['sub_service_id']
        sub_service = SubService.objects.get(id=sub_service_id)
        serializer.save(sub_service=sub_service)  # Ensure the specific service is linked to the correct sub-service



# View to retrieve, update or delete a specific specific service (GET, PUT, DELETE)
class SpecificServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecificService.objects.all()
    serializer_class = SpecificServiceSerializer
    permission_classes = [IsAdminUser]   # Adjust based on user permissions


# View to retrieve, update or delete a specific service category (GET, PUT, DELETE)
class ServiceCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminUser]  # Adjust based on user permission

# View to retrieve, update or delete a specific sub-service (GET, PUT, DELETE)
class SubServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubService.objects.all()
    serializer_class = SubServiceSerializer
    permission_classes = [IsAdminUser]   # Adjust based on user permissions

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated before logging out
    serializer_class = LogoutResponseSerializer

    def post(self, request):
        try:
            # Delete the user's token to log them out
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)







# service provider searcher here
class ServiceProviderSearchView(generics.ListAPIView):
    """
    Service Seekers can search for Service Providers based on the specific service they offer.
    """
    serializer_class = ServiceProviderProfileSerializer
    permission_classes = [AllowServiceSeekersAndUnauthenticated]


    def get(self, request, *args, **kwargs):
        # Get the lat, lng, and service_id from the request parameters
        seeker_lat = request.GET.get('lat')
        seeker_lng = request.GET.get('lng')
        service_id = request.GET.get('service_id')

        # Validate the location and service_id are provided
        if not seeker_lat or not seeker_lng or not service_id:
            return Response({"error": "Location and service_id are required"}, status=400)

        # Convert the lat and lng to float
        seeker_location = (float(seeker_lat), float(seeker_lng))

        # Fetch service providers that offer the specific service (can filter by service category, sub-service, etc.)
        providers = ServiceProviderProfile.objects.filter(specific_service_id=service_id)

        nearby_providers = []

        for provider in providers:
            # Get provider's location (latitude and longitude)
            provider_location = (provider.latitude, provider.longitude)

            # Calculate distance from seeker to provider
            distance = geodesic(seeker_location, provider_location).km  # Distance in kilometers

            # You can adjust the range here. For example, show only providers within 50 km
            if distance <= 50:  # Example: Only return providers within 50 km
                nearby_providers.append({
                    'provider': ServiceProviderProfileSerializer(provider).data,
                    'distance': distance  # Add the distance to the response
                })

        return Response({'providers': nearby_providers})




# lists users


class UserListView(generics.ListAPIView):
    """View to list all users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Allow only admin users to access this endpoint

class ServiceProviderListView(generics.ListAPIView):
    """View to list all service providers."""
    queryset = ServiceProviderProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Allow only admin users to access this endpoint

    def get_queryset(self):
        """Filter to only return users with provider profiles."""
        return User.objects.filter(provider_profile__isnull=False)

class UserDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve or delete a user by ID."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Allow only admin users to access this endpoint



class ServiceSeekerListView(generics.ListAPIView):
    """View to list all service seekers."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Restrict access to admin users

    def get_queryset(self):
        """Filter to only return users with the seeker role."""
        return User.objects.filter(role='seeker')

class ServiceSeekerDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve or delete a service seeker by ID."""
    queryset = User.objects.filter(role='seeker')  # Limit to seekers
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Restrict access to admin users
