from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    ServiceSeekerProfile,
    ServiceProviderProfile,
    ServiceCategory,
    SubService,
    SpecificService,
    PortfolioImage,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Customize the User model in the admin interface."""
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_verified')}),
    )


@admin.register(ServiceSeekerProfile)
class ServiceSeekerProfileAdmin(admin.ModelAdmin):
    """Admin for Service Seeker Profiles."""
    list_display = ('user', 'full_name', 'country', 'sex', 'education_level')
    search_fields = ('full_name', 'user__username', 'country')
    list_filter = ('sex', 'education_level')


@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    """Admin for Service Provider Profiles."""
    list_display = (
        'user',
        'full_name',
        'location',
        'country',
        'is_registered',
        'rc_number',
        'education_level',
        'service_category',
        'sub_service',
        'specific_service',
    )
    search_fields = ('full_name', 'user__username', 'location', 'country', 'rc_number')
    list_filter = ('is_registered', 'education_level', 'service_category', 'sub_service', 'specific_service')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin for Service Categories."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    """Admin for Sub Services."""
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


@admin.register(SpecificService)
class SpecificServiceAdmin(admin.ModelAdmin):
    """Admin for Specific Services."""
    list_display = ('name', 'sub_service')
    search_fields = ('name', 'sub_service__name')
    list_filter = ('sub_service',)


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    """Admin for Portfolio Images."""
    list_display = ('provider', 'image')
    search_fields = ('provider__full_name',)
