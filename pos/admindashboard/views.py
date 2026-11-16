from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Employee
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import Coalesce
from django.db import models
from datetime import date, datetime, timedelta
from stockmanager.models import Product, Wastage
from cashier.models import Invoice, InvoiceDetail, Returns

def admin_panel(request):
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    
    # Determine date range based on period parameter
    period = request.GET.get('period', 'today')
    today = date.today()
    
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == 'month':
        start_date = today.replace(day=1)
        end_date = today
    else:  # all or custom
        start_date = request.GET.get('start_date', today)
        end_date = request.GET.get('end_date', today)
        
        # Convert string dates to date objects if they're strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Get sales data
    invoice_ids = Invoice.objects.filter(
        date__range=[start_date, end_date]
    ).values_list('invoice_id', flat=True)
    
    sales_data = InvoiceDetail.objects.filter(
        invoice_id__in=invoice_ids
    ).aggregate(
        total_profit=Sum('profit'),
        total_sale_value=Sum('amount'),
        total_products=Count('product_name', distinct=True),
        total_transactions=Count('invoice_id', distinct=True)
    )

    # Get returns data
    returns_data = Returns.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_return_value=Sum('amount')
    )

    # Get wastage data
    wastage_data = Wastage.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_wastage_loss=Sum('loss')
    )

    # Get inventory statistics (not date-range dependent)
    inventory_stats = Product.objects.aggregate(
        stock_out_products=Count('id', filter=Q(quantity=0)),
        low_stock_products=Count('id', filter=Q(quantity__gt=0, quantity__lte=F('low_quantity'))),
        stock_worth_buying=Coalesce(
            Sum(F('quantity') * F('buying_price')),
            0.0,
            output_field=models.FloatField()
        ),
        stock_worth_selling=Coalesce(
            Sum(F('quantity') * F('selling_price')),
            0.0,
            output_field=models.FloatField()
        )
    )

    # Calculate statistics
    stats = {
        'total_profit': sales_data['total_profit'] or 0,
        'total_sale_value': sales_data['total_sale_value'] or 0,
        'total_return_value': returns_data['total_return_value'] or 0,
        'total_wastage_loss': wastage_data['total_wastage_loss'] or 0,
        'total_products': sales_data['total_products'] or 0,
        'total_transactions': sales_data['total_transactions'] or 0,
        'net_profit': (sales_data['total_profit'] or 0) - (wastage_data['total_wastage_loss'] or 0),
        'net_amount': (sales_data['total_sale_value'] or 0) - (returns_data['total_return_value'] or 0),
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'stock_out_products': inventory_stats['stock_out_products'],
        'low_stock_products': inventory_stats['low_stock_products'],
        'stock_worth_buying': inventory_stats['stock_worth_buying'],
        'stock_worth_selling': inventory_stats['stock_worth_selling']
    }

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'stats': stats,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'period': period
    }
    
    return render(request, 'admin.html', context)

from django.contrib import messages

def add_employee(request):

    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    # When the form is submitted (POST request)
    if request.method == 'POST':
        # Get form data
        ename = request.POST.get('t2')
        designation = request.POST.get('t3')
        dob = request.POST.get('t4')
        email = request.POST.get('t5')  # Email will also serve as username
        pno = request.POST.get('t6')  # Phone number will also serve as password
        address = request.POST.get('t7')

        # Check if email already exists
        if Employee.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists! Please use a different email.')
        else:
            # Create a new employee instance
            new_employee = Employee(
                ename=ename,
                designation=designation,
                dob=dob,
                email=email,
                pno=pno,
                address=address,
                username=email,  # Save email as username
                password=str(pno)  # Save phone number as password
            )

            # Save the new employee to the database
            new_employee.save()
            messages.success(request, 'Employee added successfully!')

        # After processing, redirect to avoid form resubmission
        return redirect('add_employee')  # Reload the page

    # Fetch all employees ordered by 'id' in descending order
    employees = Employee.objects.all().order_by('-id')

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
       
    }

    # Pass the employees to the template
    return render(request, 'addemployee.html', {'employees': employees,**context})




# View to manage employees
def memployee(request):
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    employees = Employee.objects.all().order_by('id')  # Display employees in descending order of ID

    
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
       
    }

    return render(request, 'manageemployee.html', {'employees': employees,**context})

# View to edit employee
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

def edit_employee(request, employee_id):

    name = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    ename = request.POST.get('ename')
    designation = request.POST.get('designation')
    dob = request.POST.get('dob')
    email = request.POST.get('email')
    pno = request.POST.get('pno')
    address = request.POST.get('address')
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        # Get form data
        ename = request.POST.get('ename')
        designation = request.POST.get('designation')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        pno = request.POST.get('pno')
        address = request.POST.get('address')

        # Check if email is being changed to one that already exists (excluding current employee)
        if email != employee.email and Employee.objects.filter(email=email).exclude(id=employee.id).exists():
            messages.error(request, 'Email already exists! Please use a different email.')
        else:
            # Update employee details
            employee.ename = ename
            employee.designation = designation
            employee.dob = dob
            employee.email = email
            employee.pno = pno
            employee.address = address
            employee.save()
            messages.success(request, 'Employee details updated successfully!')
            return redirect('memployee')  # Redirect back to employee management page
        
    context = {
        'name': name,
        'email': email,
        'user_id': user_id,
        'username': username,
       
    }


    return render(request, 'edit_employee.html', {'employee': employee,**context})

# View to delete employee
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    return redirect('memployee')  # Redirect back to employee management page

from stockmanager.models import Product

from django.db.models import F

def inventory(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Fetch all products
    products = Product.objects.all().order_by('id')

    # Calculate low stock and out of stock counts
    low_stock_count = Product.objects.filter(quantity__lt=F('low_quantity')).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()

    # Pass session variables and product data to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'products': products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    return render(request, 'inventory.html', context)


from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime
from cashier.models import Invoice ,InvoiceDetail
from django.db.models import Q, Sum
from stockmanager.models import Product


def past_invoice_admin(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')


    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Filter invoices based on search, start date, and end date
    invoices = Invoice.objects.all()

    if search_query:
        invoices = invoices.filter(
            Q(invoice_id__icontains=search_query) | 
            Q(customer_phone__icontains=search_query)
        )
    
    if start_date:
        invoices = invoices.filter(date__gte=datetime.strptime(start_date, "%Y-%m-%d"))
    
    if end_date:
        invoices = invoices.filter(date__lte=datetime.strptime(end_date, "%Y-%m-%d"))

    # Annotate with total profit for each invoice
    invoices = invoices.annotate(
        total_profit=Sum('products__profit')
    )

    # Pagination
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'invoicehistoryadmin.html', {
        'invoices': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username
    })

def view_invoice_admin(request, invoice_id):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    
    
    # Fetch the invoice based on the invoice_id
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    
    # Calculate total profit for this invoice
    total_profit = InvoiceDetail.objects.filter(invoice_id=invoice).aggregate(
        total_profit=Sum('profit')
    )['total_profit'] or 0.00
    
    # Add total_profit to invoice object
    invoice.total_profit = total_profit
    
    # Fetch related invoice details
    invoice_details = InvoiceDetail.objects.filter(invoice_id=invoice)

    return render(request, 'viewinvoiceadmin.html', {
        'invoice': invoice,
        'invoice_details': invoice_details,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username
    })


from django.shortcuts import render
from django.db.models import Sum, Max, Q
from stockmanager.models import Product, Wastage
from datetime import datetime, timedelta

def wastage_report_admin(request):
     

    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    # Get today's date
    today = datetime.now().date()
    
    # Initialize default dates (both set to today)
    default_start_date = today.strftime('%Y-%m-%d')
    default_end_date = today.strftime('%Y-%m-%d')
    
    # Get filter parameters from request
    start_date = request.GET.get('start_date', default_start_date)
    end_date = request.GET.get('end_date', default_end_date)
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'loss_desc')  # Default to highest loss

    # Validate and constrain dates
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if end_date_obj > today:
            end_date_obj = today
            end_date = today.strftime('%Y-%m-%d')
        
        if start_date_obj > end_date_obj:
            start_date_obj = end_date_obj
            start_date = end_date
        
    except ValueError:
        start_date = default_start_date
        end_date = default_end_date
        start_date_obj = today
        end_date_obj = today

    # Base queryset for all products
    products = Product.objects.select_related('category').all()
    
    # Filter products by search query
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(id__icontains=search_query)
        )

    # Get aggregated wastage data with loss calculation
    wastage_data = Wastage.objects.filter(
        date__range=[start_date_obj, end_date_obj]
    ).values('product_id').annotate(
        total_quantity=Sum('quantity'),
        total_loss=Sum('loss'),  # Using the pre-calculated loss field
        last_date=Max('date')
    )

    wastage_map = {item['product_id']: item for item in wastage_data}

    # Calculate total loss across all products
    total_system_loss = sum(item['total_loss'] for item in wastage_data if item['total_loss'])

    # Prepare product data with loss information
    product_wastage = []
    for product in products:
        wastage_info = wastage_map.get(product.id, {
            'total_quantity': 0,
            'total_loss': 0,
            'last_date': None
        })
        
        product_wastage.append({
            'id': product.id,
            'name': product.product_name,
            'category': product.category.category if product.category else 'Uncategorized',
            'quantity': wastage_info['total_quantity'],
            'loss': wastage_info['total_loss'],
            'last_date': wastage_info['last_date'].strftime('%Y-%m-%d') if wastage_info['last_date'] else 'Never',
            'current_stock': product.quantity,
            'buying_price': product.buying_price
        })

    # Apply sorting
    if sort == 'loss_desc':
        product_wastage.sort(key=lambda x: x['loss'], reverse=True)
    elif sort == 'loss_asc':
        product_wastage.sort(key=lambda x: x['loss'])
    elif sort == 'quantity_desc':
        product_wastage.sort(key=lambda x: x['quantity'], reverse=True)

    context = {
        'products': product_wastage,
        'total_system_loss': total_system_loss,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'sort': sort,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username
    }
    return render(request, 'wastage_analysis_admin.html', context)

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from cashier.models import Returns
from datetime import datetime, date

def return_history_admin(request):
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Set today's date as default
    today = date.today()
    default_start_date = today.strftime('%Y-%m-%d')
    default_end_date = today.strftime('%Y-%m-%d')
    
    # Get search query and date range from request
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', default_start_date)
    end_date = request.GET.get('end_date', default_end_date)
    
    # Filter returns based on search and date range
    returns_list = Returns.objects.all().order_by('-date')
    
    if search_query:
        returns_list = returns_list.filter(
            Q(invoice_id__icontains=search_query) |
            Q(product_name__icontains=search_query)
        )
    
    # Apply date filtering
    returns_list = returns_list.filter(date__range=[start_date, end_date])
    
    # Calculate total returns amount for the selected period
    total_returns = returns_list.aggregate(total=Sum('amount'))['total'] or 0
    
    # Pagination
    paginator = Paginator(returns_list, 10)  # Show 10 returns per page
    page_number = request.GET.get('page')
    returns = paginator.get_page(page_number)
    
    context = {
        'returns': returns,
        'total_returns': total_returns,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username
    }
    
    return render(request, 'returnhistoryadmin.html', context)

from django.shortcuts import render
from django.db.models import Sum, Q ,Max
from datetime import date, datetime
from stockmanager.models import Product,Wastage
from cashier.models import Invoice, InvoiceDetail, Returns




def sales_analysis(request):

    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    
    # Set today as default date range
    today = date.today()
    default_start_date = today.strftime('%Y-%m-%d')
    default_end_date = today.strftime('%Y-%m-%d')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', default_start_date)
    end_date = request.GET.get('end_date', default_end_date)
    sort = request.GET.get('sort', 'profit_desc')

    # 1. Get all sales data (excluding returns in table)
    invoice_ids = Invoice.objects.filter(
        date__range=[start_date, end_date]
    ).values_list('invoice_id', flat=True)
    
    sales_data = InvoiceDetail.objects.filter(
        invoice_id__in=invoice_ids
    ).values('product_name').annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum('amount'),
        total_profit=Sum('profit')
    )

    # 2. Get returns data for statistics
    returns_data = Returns.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_return_quantity=Sum('quantity'),
        total_return_amount=Sum('amount')
    )

    # 3. Get wastage data for statistics
    wastage_data = Wastage.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_wastage_loss=Sum('loss')
    )

    # Prepare product data (excluding returns)
    products = []
    for sale in sales_data:
        products.append({
            'name': sale['product_name'],
            'quantity': sale['total_quantity'] or 0,
            'amount': sale['total_amount'] or 0,
            'profit': sale['total_profit'] or 0,
        })

    # Apply search/sort
    if search_query:
        products = [p for p in products if search_query.lower() in p['name'].lower()]
    
    if sort == 'profit_desc':
        products.sort(key=lambda x: x['profit'], reverse=True)
    elif sort == 'quantity_desc':
        products.sort(key=lambda x: x['quantity'], reverse=True)

    # Calculate statistics (INCLUDING returns in calculations)
    total_profit = sum(p['profit'] for p in products)
    total_sale_value = sum(p['amount'] for p in products)
    total_return_value = returns_data['total_return_amount'] or 0
    total_wastage_loss = wastage_data['total_wastage_loss'] or 0
    
    net_profit = total_profit - total_wastage_loss
    net_amount = total_sale_value - total_return_value

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'products': products,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'sort': sort,
        'stats': {
            'total_profit': total_profit,
            'net_profit': net_profit,
            'total_wastage_loss': total_wastage_loss,
            'total_sale_value': total_sale_value,
            'net_amount': net_amount,
            'total_return_value': total_return_value,
            'date_range': f"{start_date} to {end_date}"
        },
        
    }
    return render(request, 'sales_analysis.html', context)