from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'buses', views.BusViewSet, basename='bus')
router.register(r'routes', views.RouteViewSet, basename='route')
router.register(r'stops', views.BusStopViewSet, basename='stop')

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/me/', views.me, name='me'),

    # Admin
    path('admin/pending/', views.pending_approvals, name='pending-approvals'),
    path('admin/approve/<int:user_id>/', views.approve_user, name='approve-user'),
    path('admin/reject/<int:user_id>/', views.reject_user, name='reject-user'),
    path('admin/users/', views.all_users, name='all-users'),
    path('admin/stats/', views.admin_stats, name='admin-stats'),

    path('buses/<int:bus_id>/assign/', views.assign_driver, name='assign-driver'),

    # Locations
    path('location/update/', views.update_location, name='update-location'),
    path('location/buses/', views.bus_locations, name='bus-locations'),
    path('location/bus/<int:bus_id>/', views.bus_location_detail, name='bus-location-detail'),
    path('buses/active/', views.active_buses, name='active-buses'),

    # Stops
    path('stops/nearby/', views.nearby_stops, name='nearby-stops'),
    path('routes/<int:route_id>/add-stop/', views.add_stop_to_route, name='add-stop-to-route'),
    path('routes/<int:route_id>/remove-stop/<int:stop_id>/', views.remove_stop_from_route, name='remove-stop-from-route'),

    # Feedback & Complaints
    path('feedback/', views.feedback, name='feedback'),
    path('complaints/', views.complaints, name='complaints'),
    path('complaints/<int:complaint_id>/update/', views.update_complaint, name='update-complaint'),

    # Traffic
    path('traffic-blocks/', views.traffic_blocks, name='traffic-blocks'),
    path('traffic-blocks/<int:block_id>/clear/', views.clear_traffic_block, name='clear-block'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='notifications-read'),

    # Dashboards
    path('operator/dashboard/', views.operator_dashboard, name='operator-dashboard'),
    path('driver/info/', views.driver_info, name='driver-info'),
]
