from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index_view(request):
    """Root URL - redirect to dashboard if logged in, else login."""
    if request.session.get('bt_token'):
        return redirect('/dashboard/')
    return redirect('/login/')


def login_page(request):
    return render(request, 'core/login.html')


def register_page(request):
    return render(request, 'core/register.html')


def dashboard_page(request):
    return render(request, 'core/dashboard.html')


def map_page(request):
    return render(request, 'core/map.html')


def stops_page(request):
    return render(request, 'core/stops.html')


def routes_page(request):
    return render(request, 'core/routes.html')


def buses_page(request):
    return render(request, 'core/buses.html')


def driver_page(request):
    return render(request, 'core/driver.html')


def traffic_page(request):
    return render(request, 'core/traffic.html')


def feedback_page(request):
    return render(request, 'core/feedback.html')


def complaints_page(request):
    return render(request, 'core/complaints.html')


def approvals_page(request):
    return render(request, 'core/approvals.html')


def users_page(request):
    return render(request, 'core/users.html')


def notifications_page(request):
    return render(request, 'core/notifications.html')
