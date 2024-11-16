from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model,authenticate


from django.utils.translation import gettext as _
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, label="Password")
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove password1 and password2 from the validated_data
        validated_data.pop('password2')
        password = validated_data.pop('password1')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            role=validated_data['role']
        )
        return user



from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ServiceSeekerProfile, ServiceProviderProfile

User = get_user_model()

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

# Service Seeker Profile Serializer
class ServiceSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSeekerProfile
        fields = [
            'full_name',
            'company_name',
            'country',
            'location',
            'sex',
            'profile_picture',
            'education_level'
        ]

# Service Provider Profile Serializer
from .models import ServiceProviderProfile, ServiceSeekerProfile
from .models import ServiceProviderProfile, ServiceCategory, SubService, SpecificService
from .models import ServiceCategory, SubService, SpecificService

# ServiceCategory Serializer
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name']

# SubService Serializer
class SubServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer()  # Include the category serializer for nested representation

    class Meta:
        model = SubService
        fields = ['id', 'category', 'name']

# SpecificService Serializer
class SpecificServiceSerializer(serializers.ModelSerializer):
    sub_service = SubServiceSerializer()  # Include the sub_service serializer for nested representation

    class Meta:
        model = SpecificService
        fields = ['id', 'sub_service', 'name']

class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all(), required=False)
    sub_service = serializers.PrimaryKeyRelatedField(queryset=SubService.objects.all(), required=False)
    specific_service = serializers.PrimaryKeyRelatedField(queryset=SpecificService.objects.all(), required=False)

    class Meta:
        model = ServiceProviderProfile
        fields = '__all__'

    profile_picture = serializers.ImageField(required=False)  # Define the field as ImageField

class ServiceSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSeekerProfile
        fields = '__all__'
    profile_picture = serializers.ImageField(required=False)  # Define the field as ImageField



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active']
