from django import forms
from django.core.exceptions import ValidationError
from .models import Product, category
from django.utils import timezone

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'low_quantity', 'Return', 'tax']
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = category.objects.all()
        self.fields['category'].empty_label = "Select Category (required)"  # Updated label
        self.fields['category'].required = True  # Explicitly set as required
        self.fields['Return'].widget = forms.Select(choices=[
            ('', 'Select Return Status'),
            ('yes', 'Yes'),
            ('no', 'No')
        ])
        self.fields['Return'].initial = 'no'
        
    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if Product.objects.filter(product_name__iexact=product_name).exists():
            raise ValidationError("A product with this name already exists!")
        return product_name

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError("Please select a category")
        return category