from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (User, Bus, BusStop, Route, RouteStop, BusLocation,
                     Feedback, Complaint, TrafficBlock, Notification)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'is_superuser', 'phone', 'is_approved', 'address',
                  'license_number', 'badge_number', 'station',
                  'operator_company', 'operator_id', 'created_at']
        read_only_fields = ['is_approved', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2',
                  'first_name', 'last_name', 'phone', 'role', 'address',
                  'license_number', 'badge_number', 'station',
                  'operator_company', 'operator_id']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        role = data.get('role', 'user')
        if role not in ['user', 'driver', 'police', 'operator']:
            raise serializers.ValidationError({'role': 'Invalid role for self-registration.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled.')
        # Ensure superusers always have admin role
        if user.is_superuser and user.role != 'admin':
            user.role = 'admin'
            user.is_approved = True
            user.save(update_fields=['role', 'is_approved'])
        if user.role not in ['admin', 'user'] and not user.is_approved:
            raise serializers.ValidationError('Your account is pending admin approval.')
        data['user'] = user
        return data


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'


class RouteStopSerializer(serializers.ModelSerializer):
    stop = BusStopSerializer(read_only=True)
    stop_id = serializers.PrimaryKeyRelatedField(queryset=BusStop.objects.all(),
                                                  source='stop', write_only=True)

    class Meta:
        model = RouteStop
        fields = ['id', 'stop', 'stop_id', 'order', 'estimated_time']


class RouteSerializer(serializers.ModelSerializer):
    stops_detail = RouteStopSerializer(source='routestop_set', many=True, read_only=True)
    operator_name = serializers.CharField(source='operator.get_full_name', read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'route_number', 'origin', 'destination',
                  'is_active', 'operator', 'operator_name', 'stops_detail', 'created_at']


class BusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = ['id', 'latitude', 'longitude', 'speed', 'heading', 'timestamp']


class BusSerializer(serializers.ModelSerializer):
    current_location = serializers.SerializerMethodField()
    route_detail = RouteSerializer(source='route', read_only=True)
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)

    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'registration_number', 'capacity',
                  'route', 'route_detail', 'driver', 'driver_name', 'operator',
                  'status', 'model', 'current_location', 'created_at']

    def get_current_location(self, obj):
        loc = obj.locations.filter(is_current=True).first()
        if loc:
            return BusLocationSerializer(loc).data
        return None


class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_name', 'bus', 'route',
                  'rating', 'category', 'message', 'created_at']
        read_only_fields = ['user']


class ComplaintSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'user', 'user_name', 'bus', 'route', 'target',
                  'subject', 'description', 'status', 'admin_response',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'admin_response']


class TrafficBlockSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source='officer.get_full_name', read_only=True)

    class Meta:
        model = TrafficBlock
        fields = ['id', 'officer', 'officer_name', 'title', 'description',
                  'latitude', 'longitude', 'radius', 'severity', 'status',
                  'affected_routes', 'created_at', 'cleared_at']
        read_only_fields = ['officer', 'cleared_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
