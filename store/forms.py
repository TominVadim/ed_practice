from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Order

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['article', 'name', 'category', 'manufacturer', 'supplier', 
                 'price', 'discount_percent', 'stock_quantity', 'description', 'image_path']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price
    
    def clean_stock_quantity(self):
        quantity = self.cleaned_data.get('stock_quantity')
        if quantity < 0:
            raise forms.ValidationError('Количество не может быть отрицательным')
        return quantity
    
    def clean_discount_percent(self):
        discount = self.cleaned_data.get('discount_percent')
        if discount < 0 or discount > 100:
            raise forms.ValidationError('Скидка должна быть от 0 до 100')
        return discount
