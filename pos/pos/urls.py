"""
URL configuration for pos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from   admindashboard import views as dviews# type: ignore
from   pos import views as pos_views # type: ignore
from stockmanager import views as s_views # type: ignore
from cashier import views as c_views # type: ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admindashboard/', dviews.admin_panel,name='admin_dashboard'),
    path('addemployee/', dviews.add_employee,name='add_employee'),
    path('manageemployee/', dviews.memployee,name='memployee'),
    path('edit_employee/<int:employee_id>/', dviews.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', dviews.delete_employee, name='delete_employee'),
    path('inventory/', dviews.inventory,name='inventory'),
    path('past-invoice-admin/', dviews.past_invoice_admin, name='past_invoice_admin'),
    path('view-invoice-admin/<str:invoice_id>/', dviews.view_invoice_admin, name='view_invoice_admin'),
    path('wastage_report_admin/', dviews.wastage_report_admin, name='wastage_report_admin'),
    path('return-history-admin/',dviews.return_history_admin, name='return_history_admin'),
    path('sales_analysis/',dviews.sales_analysis, name='sales_analysis'),
    path('', pos_views.login,name='login'),
    path('stockmanager/',s_views.stockmanager,name='stockmanager'),
    path('addcategory/',s_views.add_category,name='addcategory'),
    path('managecategory/',s_views.mcategory,name='mcategory'),
    path('edit_category/<int:category_id>/', s_views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', s_views.delete_category, name='delete_category'),
    path('addproduct/', s_views.add_product, name='add_product'),
    path('manage_product/', s_views.manage_product, name='manage_product'),
    path('delete_product/<int:Product_id>/', s_views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', s_views.update_product, name='update_product'),
    path('check-product-name/', s_views.check_product_name, name='check_product_name'),
    path('manage_stock/', s_views.manage_stock, name='manage_stock'),
    path('update_stock/<int:product_id>/', s_views.update_stock, name='update_stock'),
    path('stock-performance/', s_views.stock_performance, name='stock_performance'),
    path('wastage-management/', s_views.wastage_management, name='wastage_management'),
    path('wastage_report/', s_views.wastage_report, name='wastage_report'),
    path('billingdashboard/',c_views.billingdashboard,name='bdashboard'),
    path('invoice/', c_views.invoice_view, name='invoice'),
    path('search-product/', c_views.search_product, name='search_product'),
    path('create-invoice/', c_views.create_invoice, name='create_invoice'),
    path('past-invoice/', c_views.past_invoice, name='past_invoice'),
    path('view-invoice/<str:invoice_id>/', c_views.view_invoice, name='view_invoice'),
    path('view-product/', c_views.product_inventory, name='see_product'),
    path('returns/', c_views.returns, name='returns'),
    path('facilitate_return/<str:invoice_id>/', c_views.facilitate_return, name='facilitate_return'),
    path('api/process-return/',c_views. process_return, name='process_return'),
    path('return-history/',c_views.return_history, name='return_history'),
    path('logout-cashier/', c_views.logout, name='logout'),
    
    
  

]

