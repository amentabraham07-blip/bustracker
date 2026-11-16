from django.shortcuts import render
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Invoice, InvoiceDetail
from stockmanager.models import Product

def billingdashboard(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    if not all([ename, email, user_id, username]):  # Check if any of the session variables are missing
        return redirect('login')  # Redirect to the login page (replace 'login' with your actual login URL)

    
    # Get current date and yesterday's date
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    # Get the count of invoices generated today and yesterday
    invoices_today = Invoice.objects.filter(date=today)
    invoices_yesterday = Invoice.objects.filter(date=yesterday)
    
    invoices_generated_today = invoices_today.count()
    invoices_generated_yesterday = invoices_yesterday.count()
    
    # Calculate the percentage change for invoices
    if invoices_generated_yesterday > 0:
        invoices_percentage_change = ((invoices_generated_today - invoices_generated_yesterday) / invoices_generated_yesterday) * 100
    else:
        invoices_percentage_change = 0

    # Determine status for "Invoices Generated"
    if invoices_percentage_change > 0:
        invoices_status = "more"
        invoices_change_color = 'green'
    elif invoices_percentage_change < 0:
        invoices_status = "less"
        invoices_change_color = 'red'
    else:
        invoices_status = "no change"
        invoices_change_color = 'gray'

    # Get total sales worth today and yesterday
    total_sales_today = invoices_today.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_sales_yesterday = invoices_yesterday.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    
    # Calculate the percentage change for sales
    if total_sales_yesterday > 0:
        sales_percentage_change = ((total_sales_today - total_sales_yesterday) / total_sales_yesterday) * 100
    else:
        sales_percentage_change = 0

    # Determine status for "Sales Worth"
    if sales_percentage_change > 0:
        sales_status = "more"
        sales_change_color = 'green'
    elif sales_percentage_change < 0:
        sales_status = "less"
        sales_change_color = 'red'
    else:
        sales_status = "no change"
        sales_change_color = 'gray'

    # Get the top product of the day
    product_sales = InvoiceDetail.objects.filter(invoice_id__date=today).values('product_name')\
        .annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    if product_sales:
        top_product = product_sales[0]
        top_product_name = top_product['product_name']
        top_product_quantity = top_product['total_quantity']
    else:
        top_product_name = "No sales today"
        top_product_quantity = 0
        top_product_color = 'red'  # If no sales, show in red
        top_product_change = "less"
    
    # Pass context to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'invoices_generated_today': invoices_generated_today,
        'invoices_percentage_change': invoices_percentage_change,
        'invoices_status': invoices_status,
        'invoices_change_color': invoices_change_color,
        'total_sales_today': total_sales_today,
        'sales_percentage_change': sales_percentage_change,
        'sales_status': sales_status,
        'sales_change_color': sales_change_color,
        'top_product_name': top_product_name,
        'top_product_quantity': top_product_quantity,
        'top_product_color': top_product_color if top_product_quantity == 0 else 'green',  # Default to green if sales
    }
    
    return render(request, 'billingdashboard.html', context)




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from stockmanager.models import Product
from .models import Invoice, InvoiceDetail

from django.shortcuts import render, redirect
from .models import Invoice  # Import your Invoice model

def invoice_view(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
   
    # Check if any of the session variables are missing
    if not all([ename, email, user_id, username]):  
        return redirect('login')  # Redirect to the login page (replace 'login' with your actual login URL)

    # Prepare context with session variables
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }

    # Generate next invoice ID
    last_invoice = Invoice.objects.order_by('-invoice_id').first()
    next_number = 1
    if last_invoice:
        last_number = int(last_invoice.invoice_id.split('-')[1])
        next_number = last_number + 1
    next_invoice_id = f"INV-{next_number:05d}"

    # Check if the user is authenticated before accessing `get_full_name()`
    if request.user.is_authenticated:
        user_full_name = request.user.get_full_name()
        user_username = request.user.username
    else:
        user_full_name = "Guest User"
        user_username = "Guest"

    # Pass session and user data to the template
    return render(request, 'invoice.html', {
        'next_invoice_id': next_invoice_id,
        'username': user_username,  # Using user_username here
        'ename': user_full_name,    # Using user_full_name here
        **context
    })


def search_product(request):
    query = request.GET.get('q', '')
    try:
        if query.isdigit():
            product = Product.objects.get(pk=int(query))
        else:
            product = Product.objects.get(product_name__iexact=query)
        return JsonResponse({
            'id': product.id,
            'name': product.product_name,
            'price': float(product.selling_price)
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

import json  # Add this import at the top
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from stockmanager.models import Product
from .models import Invoice, InvoiceDetail
from decimal import Decimal

@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                invoice = Invoice.objects.create(
                    customer_phone=data.get('customer_phone'),
                    total_amount=data['total_amount']
                )
                
                for item in data['products']:
                    product = Product.objects.get(pk=item['product_id'])
                    quantity = Decimal(str(item['quantity'])).quantize(Decimal('0.001'))
                    
                    if product.quantity < quantity:
                        raise Exception(f"Insufficient stock for {product.product_name}")
                    
                    InvoiceDetail.objects.create(
                        invoice_id=invoice,
                        product_name=product.product_name,
                        price=product.selling_price,
                        quantity=quantity,
                        amount=Decimal(str(product.selling_price)) * quantity
                    )
                    
                    product.quantity -= quantity
                    product.save()
                
                return JsonResponse({
                    'success': True,
                    'invoice_id': invoice.invoice_id
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Invoice

from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime
from .models import Invoice

from django.shortcuts import render
from .models import Invoice  # Import the necessary model
from django.core.paginator import Paginator
from datetime import datetime
from .models import Invoice  # Adjust this based on your actual model name
from django.db.models import Q
from stockmanager.models import Product


def past_invoice(request):
      # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    if not all([ename, email, user_id, username]):  # Check if any of the session variables are missing
        return redirect('login')  # Redirect to the login page (replace 'login' with your actual login URL)


    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username':username,
    }
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

    # Pagination
    paginator = Paginator(invoices, 10)  # Show 10 invoices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'past_invoice.html', {
        'invoices': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date ,
        **context
    })

def view_invoice(request, invoice_id):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')
    
    if not all([ename, email, user_id, username]):  # Check if any of the session variables are missing
        return redirect('login')  # Redirect to the login page (replace 'login' with your actual login URL)

    # Pass session variables to the template
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username':username,
    }
    # Fetch the invoice based on the invoice_id
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    
    # Fetch related invoice details
    invoice_details = InvoiceDetail.objects.filter(invoice_id=invoice)

    return render(request, 'viewpastinvoice.html', {
        'invoice': invoice,
        'invoice_details': invoice_details, **context
    })

from django.shortcuts import render
from django.db.models import F  # Import F for database field references
from stockmanager.models import Product  # Import the Product model

def product_inventory(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    if not all([ename, email, user_id, username]):  # Check if any of the session variables are missing
        return redirect('login')  # Redirect to the login page (replace 'login' with your actual login URL)


    # Fetch all products
    products = Product.objects.all()

    # Calculate low stock and out of stock counts
    low_stock_count = Product.objects.filter(quantity__lt=F('low_quantity')).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()

    # Combine all context data into one dictionary
    context = {
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
        'products': products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }

    return render(request, 'view_product.html', context)



from django.shortcuts import redirect

from django.contrib import messages

from django.shortcuts import redirect

def logout(request):
    # Clear all session data
    request.session.flush()  # This deletes the session from the database and clears the session cookie
    
    # Redirect to the login page with a flag to show the alert
    response = redirect('login')
    response.set_cookie('show_alert', 'true')  # Set a cookie to trigger the alert
    return response

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
from django.http import JsonResponse
from .models import Invoice, InvoiceDetail, Returns
from stockmanager.models import Product

def returns(request):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    if not all([ename, email, user_id, username]):
        return redirect('login')

    # Handle return facilitation
    if request.method == 'POST' and 'return_id' in request.POST:
        return_id = request.POST.get('return_id')
        return process_return(request, return_id)

    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

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

    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'invoices': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    return render(request, 'returns.html', context)

def facilitate_return(request, invoice_id):
    # Retrieve session variables
    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    if not all([ename, email, user_id, username]):
        return redirect('login')

    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    invoice_details = InvoiceDetail.objects.filter(invoice_id=invoice_id)
    
    # Filter only products eligible for return
    eligible_products = []
    for detail in invoice_details:
        try:
            product = Product.objects.get(product_name=detail.product_name)
            if product.Return.lower() == 'yes':
                eligible_products.append(detail)
        except Product.DoesNotExist:
            continue

    context = {
        'invoice': invoice,
        'eligible_products': eligible_products,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    return render(request, 'facilitate_return.html', context)

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import InvoiceDetail, Returns
from stockmanager.models import Product
from datetime import datetime
import json

@csrf_exempt
@transaction.atomic
def process_return(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            return_id = data.get('return_id')
            
            if not return_id:
                return JsonResponse({'success': False, 'message': 'Missing return ID'}, status=400)
            
            # Get the invoice detail to return
            invoice_detail = get_object_or_404(InvoiceDetail, id=return_id)
            
            # Find and update the product quantity
            try:
                product = Product.objects.get(product_name=invoice_detail.product_name)
                product.quantity = float(product.quantity) + float(invoice_detail.quantity)
                product.save()
            except Product.DoesNotExist:
                pass  # Product not found, but we'll still process the return
            
            # Create return record
            Returns.objects.create(
                invoice_id=invoice_detail.invoice_id.invoice_id,
                product_name=invoice_detail.product_name,
                price=invoice_detail.price,
                quantity=invoice_detail.quantity,
                amount=invoice_detail.amount,
                date=datetime.now()
            )
            
            # Update invoice total
            invoice = invoice_detail.invoice_id
            invoice.total_amount -= invoice_detail.amount
            invoice.save()
            
            # Mark invoice detail as returned
            invoice_detail.product_name = "Returned Product"
            invoice_detail.price = None
            invoice_detail.quantity = None
            invoice_detail.amount = None
            invoice_detail.profit = None
            invoice_detail.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Return processed successfully',
                'new_total': str(invoice.total_amount)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error processing return: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method'
    }, status=405)   

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Returns
from .models import models

def return_history(request):

    ename = request.session.get('ename')
    email = request.session.get('email')
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Get search query and date range from request
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    # Filter returns based on search and date range
    returns_list = Returns.objects.all().order_by('-date')
    
    if search_query:
        returns_list = returns_list.filter(
            models.Q(invoice_id__icontains=search_query) |
            models.Q(product_name__icontains=search_query)
        )
    
    if start_date and end_date:
        returns_list = returns_list.filter(date__range=[start_date, end_date])
    elif start_date:
        returns_list = returns_list.filter(date__gte=start_date)
    elif end_date:
        returns_list = returns_list.filter(date__lte=end_date)
    
    # Pagination
    paginator = Paginator(returns_list, 10)  # Show 10 returns per page
    page_number = request.GET.get('page')
    returns = paginator.get_page(page_number)
    
    context = {
        'returns': returns,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'ename': ename,
        'email': email,
        'user_id': user_id,
        'username': username,
    }
    
    
    return render(request, 'returnhistory.html', context)