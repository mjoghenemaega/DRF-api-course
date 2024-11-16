from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Service Seeker'),
        ('provider', 'Service Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubService(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='sub_services')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class SpecificService(models.Model):
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name='specific_services')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.sub_service.name})"


class ServiceSeekerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seeker_profile"
    )
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    location = models.TextField()
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    profile_picture = models.ImageField(upload_to="profiles/service_seekers/", blank=True, null=True)
    education_level = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    rc_number = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    education_level = models.CharField(
        max_length=100,
        choices=[
            ('High School', 'High School'),
            ('Diploma', 'Diploma'),
            ('Bachelors', 'Bachelors'),
            ('Masters', 'Masters'),
            ('PhD', 'PhD'),
        ]
    )
    service_category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='providers'
    )
    sub_service = models.ForeignKey(
        SubService, on_delete=models.SET_NULL, null=True, blank=True, related_name='providers'
    )
    specific_service = models.ForeignKey(
        SpecificService, on_delete=models.SET_NULL, null=True, blank=True, related_name='providers'
    )

    def __str__(self):
        return self.full_name


class PortfolioImage(models.Model):
    provider = models.ForeignKey(
        ServiceProviderProfile, on_delete=models.CASCADE, related_name='portfolio_images'
    )
    image = models.ImageField(upload_to='portfolios/')

    def __str__(self):
        return f"Portfolio image for {self.provider.full_name}"
