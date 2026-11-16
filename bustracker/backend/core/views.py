from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import (User, Bus, BusStop, Route, RouteStop, BusLocation,
                     Feedback, Complaint, TrafficBlock, Notification)
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer,
                           BusSerializer, BusStopSerializer, RouteSerializer,
                           BusLocationSerializer, FeedbackSerializer,
                           ComplaintSerializer, TrafficBlockSerializer,
                           NotificationSerializer)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ['operator', 'admin'] and
                request.user.is_approved)


class IsPolice(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ['police', 'admin'] and
                request.user.is_approved)


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ['driver', 'admin'] and
                request.user.is_approved)


# ─── Auth ────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Registration successful.' + (
                ' Please wait for admin approval.' if user.role not in ['user'] else ' You can login now.'
            ),
            'requires_approval': user.role not in ['user']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


# ─── Admin ────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdmin])
def pending_approvals(request):
    users = User.objects.filter(is_approved=False, role__in=['driver', 'police', 'operator'])
    return Response(UserSerializer(users, many=True).data)


@api_view(['POST'])
@permission_classes([IsAdmin])
def approve_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_approved = True
        user.save()
        Notification.objects.create(
            recipient=user,
            title='Account Approved',
            message=f'Your {user.get_role_display()} account has been approved. You can now login.',
            type='system'
        )
        return Response({'message': f'{user.username} approved successfully.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdmin])
def reject_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({'message': f'{user.username} rejected.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_users(request):
    user = request.user
    role = request.GET.get('role')
    # Operators can only fetch the approved driver list (for bus assignment)
    if user.role == 'operator':
        if role == 'driver':
            users = User.objects.filter(role='driver', is_approved=True)
        else:
            return Response({'error': 'Permission denied.'}, status=403)
    elif user.role == 'admin' or user.is_superuser:
        users = User.objects.all()
        if role:
            users = users.filter(role=role)
    else:
        return Response({'error': 'Permission denied.'}, status=403)
    return Response(UserSerializer(users, many=True).data)


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_stats(request):
    return Response({
        'total_users': User.objects.filter(role='user').count(),
        'total_drivers': User.objects.filter(role='driver', is_approved=True).count(),
        'total_police': User.objects.filter(role='police', is_approved=True).count(),
        'total_operators': User.objects.filter(role='operator', is_approved=True).count(),
        'pending_approvals': User.objects.filter(is_approved=False, role__in=['driver', 'police', 'operator']).count(),
        'total_buses': Bus.objects.count(),
        'active_buses': Bus.objects.filter(status='active').count(),
        'total_routes': Route.objects.count(),
        'active_blocks': TrafficBlock.objects.filter(status='active').count(),
        'pending_complaints': Complaint.objects.filter(status='pending').count(),
    })


# ─── Bus ─────────────────────────────────────────────────────────────────────

class BusViewSet(viewsets.ModelViewSet):
    serializer_class = BusSerializer

    def get_queryset(self):
        user = self.request.user
        # Operators only see their own buses
        if user.role == 'operator':
            return Bus.objects.filter(operator=user)
        return Bus.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsOperator()]

    def perform_create(self, serializer):
        # Auto-assign operator when an operator creates a bus
        if self.request.user.role == 'operator':
            bus = serializer.save(operator=self.request.user)
        else:
            bus = serializer.save()
        # Notify driver if assigned
        if bus.driver:
            Notification.objects.create(
                recipient=bus.driver,
                title='Bus Assignment',
                message=f'You have been assigned to bus {bus.bus_number}' +
                        (f' on Route {bus.route.route_number}' if bus.route else '') + '.',
                type='system'
            )

    def perform_update(self, serializer):
        old_bus = self.get_object()
        old_driver = old_bus.driver
        bus = serializer.save()
        # Notify newly assigned driver
        if bus.driver and bus.driver != old_driver:
            Notification.objects.create(
                recipient=bus.driver,
                title='Bus Assignment',
                message=f'You have been assigned to bus {bus.bus_number}' +
                        (f' on Route {bus.route.route_number}' if bus.route else '') + '.',
                type='system'
            )
        # Notify unassigned driver
        if old_driver and old_driver != bus.driver:
            Notification.objects.create(
                recipient=old_driver,
                title='Bus Unassignment',
                message=f'You have been removed from bus {bus.bus_number}.',
                type='system'
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_buses(request):
    buses = Bus.objects.filter(status='active').select_related('route', 'driver')
    return Response(BusSerializer(buses, many=True).data)


@api_view(['PATCH'])
@permission_classes([IsOperator])
def assign_driver(request, bus_id):
    """Assign or unassign a driver from a bus."""
    try:
        bus = Bus.objects.get(id=bus_id)
    except Bus.DoesNotExist:
        return Response({'error': 'Bus not found.'}, status=404)
    # Operators can only manage their own buses
    if request.user.role == 'operator' and bus.operator != request.user:
        return Response({'error': 'Permission denied.'}, status=403)

    old_driver = bus.driver
    driver_id = request.data.get('driver_id')
    route_id  = request.data.get('route_id')

    if driver_id is not None:
        if driver_id == '' or driver_id == 0:
            bus.driver = None
        else:
            try:
                driver = User.objects.get(id=driver_id, role='driver', is_approved=True)
                bus.driver = driver
            except User.DoesNotExist:
                return Response({'error': 'Driver not found or not approved.'}, status=404)

    if route_id is not None:
        if route_id == '' or route_id == 0:
            bus.route = None
        else:
            try:
                from .models import Route as RouteModel
                route = RouteModel.objects.get(id=route_id)
                bus.route = route
            except RouteModel.DoesNotExist:
                return Response({'error': 'Route not found.'}, status=404)

    bus.save()

    # Notify newly assigned driver
    if bus.driver and bus.driver != old_driver:
        Notification.objects.create(
            recipient=bus.driver,
            title='Bus Assignment',
            message=f'You have been assigned to bus {bus.bus_number}' +
                    (f' on Route {bus.route.route_number}' if bus.route else '') + '.',
            type='system'
        )
    # Notify removed driver
    if old_driver and old_driver != bus.driver:
        Notification.objects.create(
            recipient=old_driver,
            title='Bus Unassignment',
            message=f'You have been removed from bus {bus.bus_number}.',
            type='system'
        )

    return Response(BusSerializer(bus).data)


# ─── Bus Location ─────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsDriver])
def update_location(request):
    driver = request.user
    try:
        bus = Bus.objects.get(driver=driver)
    except Bus.DoesNotExist:
        return Response({'error': 'No bus assigned to this driver.'}, status=404)

    lat = request.data.get('latitude')
    lng = request.data.get('longitude')
    speed = request.data.get('speed', 0)
    heading = request.data.get('heading', 0)

    if lat is None or lng is None:
        return Response({'error': 'latitude and longitude required.'}, status=400)

    BusLocation.objects.create(
        bus=bus, latitude=lat, longitude=lng,
        speed=speed, heading=heading, is_current=True
    )
    bus.status = 'active'
    bus.save()

    return Response({'message': 'Location updated.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bus_locations(request):
    buses = Bus.objects.filter(status='active')
    data = []
    for bus in buses:
        loc = bus.locations.filter(is_current=True).first()
        if loc:
            data.append({
                'bus_id': bus.id,
                'bus_number': bus.bus_number,
                'route': bus.route.route_number if bus.route else None,
                'route_name': str(bus.route) if bus.route else 'Unassigned',
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'speed': loc.speed,
                'heading': loc.heading,
                'last_updated': loc.timestamp,
            })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bus_location_detail(request, bus_id):
    try:
        bus = Bus.objects.get(id=bus_id)
    except Bus.DoesNotExist:
        return Response({'error': 'Bus not found.'}, status=404)
    loc = bus.locations.filter(is_current=True).first()
    if not loc:
        return Response({'error': 'No location data.'}, status=404)
    return Response(BusLocationSerializer(loc).data)


# ─── Routes ──────────────────────────────────────────────────────────────────

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsOperator()]

    def perform_create(self, serializer):
        if self.request.user.role == 'operator':
            serializer.save(operator=self.request.user)
        else:
            serializer.save()


@api_view(['POST'])
@permission_classes([IsOperator])
def add_stop_to_route(request, route_id):
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({'error': 'Route not found.'}, status=404)
    stop_id = request.data.get('stop_id')
    order = request.data.get('order', 1)
    estimated_time = request.data.get('estimated_time', '')
    try:
        stop = BusStop.objects.get(id=stop_id)
    except BusStop.DoesNotExist:
        return Response({'error': 'Stop not found.'}, status=404)
    rs, created = RouteStop.objects.get_or_create(
        route=route, stop=stop,
        defaults={'order': order, 'estimated_time': estimated_time}
    )
    return Response({'message': 'Stop added.' if created else 'Stop already in route.'})


@api_view(['DELETE'])
@permission_classes([IsOperator])
def remove_stop_from_route(request, route_id, stop_id):
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({'error': 'Route not found.'}, status=404)
    if request.user.role == 'operator' and route.operator != request.user:
        return Response({'error': 'Permission denied.'}, status=403)
    deleted, _ = RouteStop.objects.filter(route=route, stop_id=stop_id).delete()
    if deleted:
        return Response({'message': 'Stop removed from route.'})
    return Response({'error': 'Stop not found in route.'}, status=404)


# ─── Bus Stops ────────────────────────────────────────────────────────────────

class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nearby_stops(request):
    lat = float(request.GET.get('lat', 0))
    lng = float(request.GET.get('lng', 0))
    radius = float(request.GET.get('radius', 2.0))  # km
    import math
    stops = BusStop.objects.all()
    nearby = []
    for stop in stops:
        dlat = abs(stop.latitude - lat) * 111
        dlng = abs(stop.longitude - lng) * 111 * math.cos(math.radians(lat))
        dist = math.sqrt(dlat**2 + dlng**2)
        if dist <= radius:
            nearby.append({**BusStopSerializer(stop).data, 'distance_km': round(dist, 2)})
    nearby.sort(key=lambda x: x['distance_km'])
    return Response(nearby)


# ─── Feedback ─────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def feedback(request):
    if request.method == 'GET':
        if request.user.role == 'admin':
            feedbacks = Feedback.objects.all().order_by('-created_at')
        elif request.user.role == 'operator':
            feedbacks = Feedback.objects.filter(bus__operator=request.user).order_by('-created_at')
        else:
            feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
        return Response(FeedbackSerializer(feedbacks, many=True).data)

    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# ─── Complaints ───────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def complaints(request):
    if request.method == 'GET':
        if request.user.role == 'admin':
            data = Complaint.objects.all().order_by('-created_at')
        elif request.user.role == 'police':
            data = Complaint.objects.filter(target='police').order_by('-created_at')
        else:
            data = Complaint.objects.filter(user=request.user).order_by('-created_at')
        return Response(ComplaintSerializer(data, many=True).data)

    serializer = ComplaintSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def update_complaint(request, complaint_id):
    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
    complaint.status = request.data.get('status', complaint.status)
    complaint.admin_response = request.data.get('admin_response', complaint.admin_response)
    complaint.save()
    if complaint.status in ['resolved', 'rejected']:
        Notification.objects.create(
            recipient=complaint.user,
            title=f'Complaint {complaint.status.title()}',
            message=f'Your complaint "{complaint.subject}" has been {complaint.status}.',
            type='complaint'
        )
    return Response(ComplaintSerializer(complaint).data)


# ─── Traffic Blocks ───────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def traffic_blocks(request):
    if request.method == 'GET':
        blocks = TrafficBlock.objects.filter(status='active').order_by('-created_at')
        return Response(TrafficBlockSerializer(blocks, many=True).data)

    if request.user.role not in ['police', 'admin']:
        return Response({'error': 'Permission denied.'}, status=403)

    serializer = TrafficBlockSerializer(data=request.data)
    if serializer.is_valid():
        block = serializer.save(officer=request.user)
        # Notify drivers
        drivers = User.objects.filter(role='driver', is_approved=True)
        for driver in drivers:
            Notification.objects.create(
                recipient=driver,
                title=f'⚠️ Traffic Block: {block.title}',
                message=f'Severity: {block.severity.upper()} - {block.description}',
                type='traffic'
            )
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsPolice])
def clear_traffic_block(request, block_id):
    try:
        block = TrafficBlock.objects.get(id=block_id)
    except TrafficBlock.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
    if block.officer != request.user and request.user.role != 'admin':
        return Response({'error': 'Permission denied.'}, status=403)
    block.clear()
    return Response({'message': 'Traffic block cleared.'})


# ─── Notifications ────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    notifs = Notification.objects.filter(recipient=request.user, is_read=False)
    return Response(NotificationSerializer(notifs, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return Response({'message': 'All notifications marked as read.'})


# ─── Operator Dashboard ───────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsOperator])
def operator_dashboard(request):
    operator = request.user
    buses = Bus.objects.filter(operator=operator)
    routes = Route.objects.filter(operator=operator)
    feedbacks = Feedback.objects.filter(bus__operator=operator)
    avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks) if feedbacks else 0
    return Response({
        'total_buses': buses.count(),
        'active_buses': buses.filter(status='active').count(),
        'total_routes': routes.count(),
        'active_routes': routes.filter(is_active=True).count(),
        'total_feedback': feedbacks.count(),
        'average_rating': round(avg_rating, 1),
    })


# ─── Driver Info ─────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsDriver])
def driver_info(request):
    driver = request.user
    try:
        bus = Bus.objects.get(driver=driver)
        bus_data = BusSerializer(bus).data
    except Bus.DoesNotExist:
        bus_data = None
    blocks = TrafficBlock.objects.filter(status='active').order_by('-created_at')
    return Response({
        'driver': UserSerializer(driver).data,
        'assigned_bus': bus_data,
        'active_traffic_blocks': TrafficBlockSerializer(blocks, many=True).data,
    })
