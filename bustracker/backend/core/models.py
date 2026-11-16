from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'Passenger'),
        ('driver', 'Driver'),
        ('police', 'Police Officer'),
        ('operator', 'Bus Operator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    is_approved = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Driver-specific
    license_number = models.CharField(max_length=50, blank=True)
    # Police-specific
    badge_number = models.CharField(max_length=50, blank=True)
    station = models.CharField(max_length=100, blank=True)
    # Operator-specific
    operator_company = models.CharField(max_length=100, blank=True)
    operator_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def save(self, *args, **kwargs):
        # Superusers always get admin role and approval
        if self.is_superuser:
            self.role = 'admin'
        if self.role in ['admin', 'user'] or self.is_superuser:
            self.is_approved = True
        super().save(*args, **kwargs)


class BusStop(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=200)
    route_number = models.CharField(max_length=20, unique=True)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    stops = models.ManyToManyField(BusStop, through='RouteStop', blank=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='operated_routes',
                                  limit_choices_to={'role': 'operator'})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route {self.route_number}: {self.origin} → {self.destination}"


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    estimated_time = models.CharField(max_length=20, blank=True, help_text="e.g. 10 mins")

    class Meta:
        ordering = ['order']
        unique_together = ['route', 'stop']


class Bus(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]
    bus_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=30, unique=True)
    capacity = models.PositiveIntegerField(default=50)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='buses')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='assigned_bus',
                                limit_choices_to={'role': 'driver'})
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='owned_buses',
                                  limit_choices_to={'role': 'operator'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    model = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus {self.bus_number}"


class BusLocation(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(default=0, help_text="km/h")
    heading = models.FloatField(default=0, help_text="degrees")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.is_current:
            BusLocation.objects.filter(bus=self.bus, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    CATEGORY_CHOICES = [
        ('service', 'Service Quality'),
        ('driver', 'Driver Behavior'),
        ('cleanliness', 'Cleanliness'),
        ('punctuality', 'Punctuality'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} - {self.rating}★"


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    TARGET_CHOICES = [
        ('operator', 'Bus Operator'),
        ('police', 'Traffic Police'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='operator')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint: {self.subject} by {self.user.username}"


class TrafficBlock(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cleared', 'Cleared'),
    ]
    officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='traffic_blocks',
                                 limit_choices_to={'role': 'police'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(default=500, help_text="Radius in meters")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    affected_routes = models.ManyToManyField(Route, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cleared_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Traffic Block: {self.title} ({self.severity})"

    def clear(self):
        self.status = 'cleared'
        self.cleared_at = timezone.now()
        self.save()


class Notification(models.Model):
    TYPE_CHOICES = [
        ('traffic', 'Traffic Alert'),
        ('route', 'Route Update'),
        ('system', 'System'),
        ('complaint', 'Complaint Update'),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
                                   null=True, blank=True)
    role_target = models.CharField(max_length=20, blank=True, help_text="Send to all of this role")
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
