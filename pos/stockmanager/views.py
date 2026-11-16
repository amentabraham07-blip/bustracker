from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from .models import category
from .models import Product
from django import forms
from .forms import ProductForm
from django.contrib import messages


from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import Coalesce
from django.db import models
from datetime import date, datetime, timedelta
from stockmanager.models import Product, Wastage
from cashier.models import Invoice, InvoiceDetail, Returns

def stockmanager(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Determine date range based on period parameter
    period = request.GET.get('period', 'today')
    today = timezone.now().date()
    
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
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Time-based statistics
    # Get sales data
    invoice_ids = Invoice.objects.filter(
        date__range=[start_date, end_date]
    ).values_list('invoice_id', flat=True)
    
    sales_data = InvoiceDetail.objects.filter(
        invoice_id__in=invoice_ids
    ).aggregate(
        total_sale_quantity=Sum('quantity'),
        total_sale_value=Sum('amount'),
        products_sold=Count('product_name', distinct=True)
    )

    # Get returns data
    returns_data = Returns.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_return_quantity=Sum('quantity'),
        total_return_value=Sum('amount')
    )

    # Get wastage data
    wastage_data = Wastage.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total_wastage_quantity=Sum('quantity'),
        total_wastage_loss=Sum('loss')
    )

    # General statistics (not time-based)
    # Calculate dead products (not sold in last 30 days) using a subquery
    recently_sold_products = InvoiceDetail.objects.filter(
        invoice_id__date__gte=today-timedelta(days=30)
    ).values_list('product_name', flat=True).distinct()
    
    inventory_stats = {
        'dead_products': Product.objects.exclude(
            product_name__in=recently_sold_products
        ).count(),
        'out_of_stock': Product.objects.filter(quantity=0).count(),
        'low_stock': Product.objects.filter(quantity__gt=0, quantity__lte=F('low_quantity')).count(),
        'total_inventory_value': Product.objects.aggregate(
            total=Coalesce(
                Sum(F('quantity') * F('selling_price')),
                0.0,
                output_field=models.FloatField()
            )
        )['total']
    }

    # Prepare statistics
    time_stats = {
        'wastage_quantity': wastage_data['total_wastage_quantity'] or 0,
        'wastage_value': wastage_data['total_wastage_loss'] or 0,
        'products_sold_quantity': sales_data['total_sale_quantity'] or 0,
        'products_sold_value': sales_data['total_sale_value'] or 0,
        'total_sales_quantity': sales_data['total_sale_quantity'] or 0,
        'total_sales_value': sales_data['total_sale_value'] or 0,
        'returns_quantity': returns_data['total_return_quantity'] or 0,
        'returns_value': returns_data['total_return_value'] or 0,
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    }

    general_stats = {
        'dead_products': inventory_stats['dead_products'],
        'out_of_stock': inventory_stats['out_of_stock'],
        'low_stock': inventory_stats['low_stock'],
        'total_inventory_value': inventory_stats['total_inventory_value']
    }

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'time_stats': time_stats,
        'general_stats': general_stats,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'period': period
    }

    return render(request, 'stockmanager.html', context)

def add_category(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    
    # When the form is submitted (POST request)
    if request.method == 'POST':
        # Get form data
        category_name = request.POST.get('t1')  # Renamed the variable to avoid conflict

        # Create a new category instance
        new_category = category(  # Make sure your model is named "Category" (assuming it's the correct model)
            category=category_name,
        )

        # Save the new category to the database
        new_category.save()

        # After saving, redirect to avoid form resubmission
        return redirect('addcategory')  # Reload the page

    # Fetch all categories ordered by 'id' in descending order
    categories = category.objects.all().order_by('-id')  # Renamed to avoid conflict with variable name

    # Pass the categories to the template
    return render(request, 'addcategory.html', {'categories': categories, **context})

def mcategory(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    categories = category.objects.all().order_by('id')  # Display categories in descending order of ID
    return render(request, 'managecategory.html', {'categories': categories, **context})

# View to edit employee
def edit_category(request, category_id):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    categories = get_object_or_404(category, pk=category_id)

    if request.method == 'POST':
        # Update employee details
        categories.category = request.POST.get('category')
        
        categories.save()
        return redirect('mcategory')  # Redirect back to employee management page

    return render(request, 'edit_category.html', {'categories': categories,**context})

# View to delete employee
def delete_category(request, category_id):
    categories = get_object_or_404(category, pk=category_id)
    categories.delete()
    return redirect('mcategory')  # Redirect back to manage employee



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, category
from .forms import ProductForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.utils import timezone

def add_product(request):
    # Retrieve session variables
    username = request.session.get('username')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # Set default values
            product.buying_price = 0
            product.selling_price = 0
            product.quantity = 0
            product.date = None  # Will be set by signal when quantity changes from 0
            
            try:
                product.save()
                messages.success(request, f'Product added successfully!')
                return redirect('add_product')
            except Exception as e:
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            # Form is invalid - errors will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    products = Product.objects.all().order_by("-id")
    
    context = {
        'username': username,
        'form': form,
        'products': products,
    }
    return render(request, 'add_product.html', context)

from django.db.models import Q

from django.db.models import Q

def manage_product(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Initialize products queryset
    products = Product.objects.all().order_by('id')

    # Handle search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(id__icontains=search_query) |
            Q(product_name__icontains=search_query) |
            Q(category__category__icontains=search_query)  
        )

    # Pass session variables and products to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'products': products,
    }
    return render(request, 'ustocks.html', context)


def delete_product(request, Product_id):
    products = get_object_or_404(Product, pk=Product_id)
    products.delete()
    return redirect('manage_product') 


from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

def check_product_name(request):
    name = request.GET.get('name', '').strip()
    product_id = request.GET.get('product_id', '')
    
    if not name:
        return JsonResponse({'exists': False})
    
    # Check if name exists excluding current product
    query = Product.objects.filter(product_name__iexact=name)
    if product_id:
        query = query.exclude(id=product_id)
    
    exists = query.exists()
    return JsonResponse({'exists': exists})

def update_product(request, product_id):
    # Retrieve session variables
    username = request.session.get('username')
    
    # Fetch the product to be updated
    product = get_object_or_404(Product, pk=product_id)
    categories = category.objects.all()

    if request.method == "POST":
        product_name = request.POST.get('product_name', '').strip()
        category_id = request.POST.get('category')
        low_quantity = request.POST.get('low_quantity')
        tax = request.POST.get('tax')
        return_status = request.POST.get('Return')

        # Check if product name exists (case-insensitive, excluding current product)
        if product_name and product_name.lower() != product.product_name.lower():
            if Product.objects.filter(
                Q(product_name__iexact=product_name) & 
                ~Q(id=product_id)
            ).exists():
                messages.error(request, 'A product with this name already exists!')
                return render(request, 'edit_product.html', {
                    'product': product,
                    'categories': categories,
                    'username': username,
                })

        # Update fields
        if product_name:
            product.product_name = product_name
        
        if category_id:
            try:
                product.category = category.objects.get(id=category_id)
            except category.DoesNotExist:
                pass
        
        if low_quantity:
            product.low_quantity = float(low_quantity)

        if tax:
            product.tax = int(tax)

        if return_status:
            product.Return = return_status

        try:
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_product')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    return render(request, 'edit_product.html', {
        'product': product,
        'categories': categories,
        'username': username,
    })

from django.db.models import F

def manage_stock(request):
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
    return render(request, 'manage_stock.html', context)


from django.http import JsonResponse
from decimal import Decimal


def update_stock(request, product_id):

     # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username':username,
    }
    # Get the product from the database
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        # Get the data from the form
        buying_price = request.POST.get('buying_price')
        selling_price = request.POST.get('selling_price')
        quantity = request.POST.get('quantity')

        # Update the buying price, selling price, and quantity if valid
        if buying_price and selling_price:
            if float(selling_price) < float(buying_price):
                # If selling price is less than buying price, return a validation error
                return JsonResponse({'error': 'Selling price cannot be less than buying price.'}, status=400)

            product.buying_price = float(buying_price)
            product.selling_price = float(selling_price)

        if quantity:
            # Add the entered quantity to the existing quantity in the database
            product.quantity += Decimal(quantity)

        # Save the product
        product.save()

        # Redirect to the product list or another relevant page
        return redirect('manage_stock')  # Change 'product_list' to the correct URL name

    return render(request, 'update_stock.html', {'product': product,**context} ,)

from django.db.models import Sum, F, Q
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Product
from cashier.models import  Invoice, InvoiceDetail


def stock_performance(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Get today's date and the start of the month
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Fetch all products excluding those with date = null
    products = Product.objects.exclude(date__isnull=True)

    # Fetch today's invoices
    today_invoices = Invoice.objects.filter(date=today)
    today_invoice_ids = today_invoices.values_list('invoice_id', flat=True)

    # Fetch this month's invoices
    month_invoices = Invoice.objects.filter(date__gte=start_of_month, date__lte=today)
    month_invoice_ids = month_invoices.values_list('invoice_id', flat=True)

    # Helper function to calculate sales for a given time period
    def calculate_sales(invoice_ids):
        sales_data = InvoiceDetail.objects.filter(invoice_id__in=invoice_ids).values('product_name').annotate(
            total_quantity=Sum('quantity'))
        return {item['product_name']: item['total_quantity'] for item in sales_data}

    # Calculate sales for today and this month
    today_sales = calculate_sales(today_invoice_ids)
    month_sales = calculate_sales(month_invoice_ids)

    # Prepare data for each sorting option
    def prepare_sales_data(sales_data, products):
        data = []
        for product in products:
            quantity_sold = sales_data.get(product.product_name, 0)
            data.append({
                'product_id': product.id,
                'product_name': product.product_name,
                'quantity_sold': quantity_sold,
            })
        # Sort in descending order of quantity_sold
        return sorted(data, key=lambda x: x['quantity_sold'], reverse=True)

    def prepare_dead_stock_data(sales_data, products, time_period):
        data = []
        for product in products:
            if product.quantity > 0:  # Exclude out-of-stock products
                if time_period == 'today':
                    if product.date != today:  # Exclude products with date = today
                        if product.product_name not in sales_data:
                            data.append({
                                'product_id': product.id,
                                'product_name': product.product_name,
                            })
                elif time_period == 'month':
                    if product.date < today - timedelta(days=15):  # Exclude products within the last 15 days
                        if product.product_name not in sales_data:
                            data.append({
                                'product_id': product.id,
                                'product_name': product.product_name,
                            })
        return data

    # Prepare data for each sorting option
    sales_today = prepare_sales_data(today_sales, products)
    sales_this_month = prepare_sales_data(month_sales, products)
    dead_products_today = prepare_dead_stock_data(today_sales, products, 'today')
    dead_stocks_this_month = prepare_dead_stock_data(month_sales, products, 'month')

    # Pass data to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'sales_today': sales_today,
        'sales_this_month': sales_this_month,
        'dead_products_today': dead_products_today,
        'dead_stocks_this_month': dead_stocks_this_month,
    }
    return render(request, 'stockperfomance.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Wastage

def wastage_management(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
       
    }

    products = []
    search_query = ""
    
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        wasted_quantity = request.POST.get('wasted_quantity')
        reason = request.POST.get('reason')
        
        try:
            product = Product.objects.get(id=product_id)
            wasted_quantity = float(wasted_quantity)
            
            if wasted_quantity <= 0:
                messages.error(request, "Wasted quantity must be positive")
            elif wasted_quantity > float(product.quantity):
                messages.error(request, "Wasted quantity cannot exceed available stock")
            else:
                # Update product quantity
                product.quantity = float(product.quantity) - wasted_quantity
                product.save()
                
                # Create wastage record
                Wastage.objects.create(
                    product_id=product.id,
                    product_name=product.product_name,
                    quantity=wasted_quantity,
                    price=product.buying_price,
                    reason=reason
                )
                
                messages.success(request, f"Wastage recorded for {product.product_name}")
                return redirect('wastage_management')
                
        except Product.DoesNotExist:
            messages.error(request, "Product not found")
        except ValueError:
            messages.error(request, "Invalid quantity entered")
    
    # Handle search
    if 'search' in request.GET:
        search_query = request.GET.get('search', '').strip()
        if search_query:
            try:
                # Search by ID if query is numeric
                if search_query.isdigit():
                    products = Product.objects.filter(id=int(search_query))
                else:
                    # Search by name
                    products = Product.objects.filter(product_name__icontains=search_query)
            except ValueError:
                products = []
    
    return render(request, 'wastage_management.html', {
        'products': products,
        'search_query': search_query,
         **context
       
    })

from django.shortcuts import render
from django.db.models import Sum, Max, Q
from .models import Product, Wastage
from datetime import datetime, timedelta

def wastage_report(request):
     # Retrieve session variables
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
    sort = request.GET.get('sort', 'quantity_desc')  # Default to most wastage

    # Validate and constrain dates
    try:
        # Parse dates to ensure they're valid
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Ensure end date doesn't exceed today
        if end_date_obj > today:
            end_date_obj = today
            end_date = today.strftime('%Y-%m-%d')
        
        # Ensure start date doesn't exceed end date
        if start_date_obj > end_date_obj:
            start_date_obj = end_date_obj
            start_date = end_date
        
    except ValueError:
        # If invalid dates provided, default to today
        start_date = default_start_date
        end_date = default_end_date
        start_date_obj = today
        end_date_obj = today

    # Base queryset for all products
    products = Product.objects.select_related('category').all()
    
    
    # Filter products by search query if provided
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(id__icontains=search_query)
        )

    # Prepare date filters for wastage
    wastage_filters = {
        'date__range': [start_date_obj, end_date_obj]
    }

    # Get aggregated wastage data
    wastage_data = Wastage.objects.filter(**wastage_filters).values('product_id').annotate(
        total_quantity=Sum('quantity'),
        last_date=Max('date')
    )

    # Create a dictionary for quick wastage lookup
    wastage_map = {item['product_id']: item for item in wastage_data}

    # Prepare final data with all products
    product_wastage = []
    for product in products:
        wastage_info = wastage_map.get(product.id, {
            'total_quantity': 0,
            'last_date': None
        })
        
        product_wastage.append({
            'id': product.id,
            'name': product.product_name,
            'category': product.category.category if product.category else 'Uncategorized',
            'total_wastage': wastage_info['total_quantity'],
            'last_date': wastage_info['last_date'].strftime('%Y-%m-%d') if wastage_info['last_date'] else 'Never',
            'current_stock': product.quantity
        })

    # Apply sorting
    if sort == 'quantity_desc':
        product_wastage.sort(key=lambda x: x['total_wastage'], reverse=True)
    elif sort == 'quantity_asc':
        product_wastage.sort(key=lambda x: x['total_wastage'])

    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'products': product_wastage,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'sort': sort,
        
    }
    return render(request, 'wastage_analysis.html', context)