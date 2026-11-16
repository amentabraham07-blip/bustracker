from django.shortcuts import render, redirect
from django.contrib import messages
from admindashboard.models import Employee

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Try to get the employee by username
        try:
            employee = Employee.objects.get(username=username)

            # Check if the password matches the employee's phone number
            if str(employee.password) == password:
                # Set session variables
                request.session['ename'] = employee.ename
                request.session['email'] = employee.email
                request.session['id'] = employee.id
                request.session['username'] = employee.username
                
                # Redirect to their respective dashboard based on the designation
                if employee.designation.lower() == 'stock manager':
                    return redirect('stockmanager')
                elif employee.designation.lower() == 'admin':
                    return redirect('admin_dashboard')
                elif employee.designation.lower() == 'biller':
                    return redirect('bdashboard')
                else:
                    # If the designation is not recognized
                    messages.error(request, 'Invalid designation!')
                    return redirect('login')
            else:
                # If the password is incorrect
                messages.error(request, 'Username or password incorrect!')
                return redirect('login')
        except Employee.DoesNotExist:
            # If no employee is found with the provided username
            messages.error(request, 'Username or password incorrect!')
            return redirect('login')

    return render(request, 'login.html')
