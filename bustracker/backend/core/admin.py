from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (User, Bus, BusStop, Route, RouteStop, BusLocation,
                     Feedback, Complaint, TrafficBlock, Notification)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_approved', 'is_active', 'created_at']
    list_filter = ['role', 'is_approved', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Bus Tracker', {'fields': ('role', 'phone', 'is_approved', 'address',
                                     'license_number', 'badge_number', 'station',
                                     'operator_company', 'operator_id')}),
    )
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
    approve_selected.short_description = 'Approve selected users'


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'registration_number', 'route', 'driver', 'status']
    list_filter = ['status']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'name', 'origin', 'destination', 'is_active']


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'target', 'status', 'created_at']
    list_filter = ['status', 'target']


@admin.register(TrafficBlock)
class TrafficBlockAdmin(admin.ModelAdmin):
    list_display = ['title', 'officer', 'severity', 'status', 'created_at']
    list_filter = ['severity', 'status']


admin.site.register(Feedback)
admin.site.register(BusLocation)
admin.site.register(Notification)
admin.site.register(RouteStop)
