from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import page_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),

    # Frontend pages served by Django templates
    path('', page_views.index_view, name='index'),
    path('login/', page_views.login_page, name='login'),
    path('register/', page_views.register_page, name='register'),
    path('dashboard/', page_views.dashboard_page, name='dashboard'),
    path('map/', page_views.map_page, name='map'),
    path('stops/', page_views.stops_page, name='stops'),
    path('routes/', page_views.routes_page, name='routes'),
    path('buses/', page_views.buses_page, name='buses'),
    path('driver/', page_views.driver_page, name='driver'),
    path('traffic/', page_views.traffic_page, name='traffic'),
    path('feedback/', page_views.feedback_page, name='feedback'),
    path('complaints/', page_views.complaints_page, name='complaints'),
    path('approvals/', page_views.approvals_page, name='approvals'),
    path('users/', page_views.users_page, name='users'),
    path('notifications/', page_views.notifications_page, name='notifications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
