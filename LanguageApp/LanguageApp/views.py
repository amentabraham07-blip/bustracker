from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm   # 
from AdminDashboard import models

def register(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        roll = request.POST.get('roll')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')
        
        # Set status based on role
        if roll == 'student':
            status = 'approved'
        elif roll == 'mentor':
            status = 'pending'
        else:
            status = 'pending'
        
        # Create user
        user = User.objects.create(
            name=name,
            address=address,
            email=email,
            roll=roll,
            status=status,
            dob=dob,
            phone=phone,
            username=username,
            password=password  # Plain text as per your model
        )
        
        messages.success(request, "Registration successful! Please login to proceed.")
        return redirect('login')
    
    return render(request, 'register.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from AdminDashboard.models import User


def login(request):
    if request.method == "POST":
        login_input = request.POST.get("login")   # username or email
        password = request.POST.get("password")

        try:
            user = User.objects.get(
                Q(username=login_input) | Q(email=login_input)
            )
        except User.DoesNotExist:
            messages.error(request, "Username or Email does not exist.")
            return redirect("login")

        # password check (plain text as per your model)
        if user.password != password:
            messages.error(request, "Incorrect password.")
            return redirect("login")

        # status check
        if user.status != "approved":
            messages.warning(request, "Profile under verification.")
            return redirect("login")

        #  store session variables
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["email"] = user.email
        request.session["name"] = user.name
        request.session["roll"] = user.roll

        # role-based redirect
        if user.roll == "mentor":
            return redirect("/expertdashboard")
        elif user.roll == "student":
            return redirect("/student-dashboard")
        elif user.roll == "admin":
            return redirect("/admindashboard")
        else:
            messages.error(request, "Invalid user role.")
            return redirect("login")

    return render(request, "login.html")


