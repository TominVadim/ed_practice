from django import forms
from .models import Service, Pet, Order, OrderService

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'price', 'discount'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'})
        }
        
        
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'type_of_pet', 'breed', 'weight', 'birth_date', 'owner'
        ]
        widgets = {
            'name': forms.TextInput(),
            'type_of_pet': forms.Select(),
            'breed': forms.Select(),
            'weight': forms.NumberInput(),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'owner': forms.Select()
        }
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user', 'total_amount'
        ]
        widgets = {
            'user': forms.Select(),
            'total_amount': forms.NumberInput(),
        }
        
class OrderServiceForm(forms.ModelForm):
    class Meta:
        model = OrderService
        fields = [
            'order', 'service', 'quantity', 'price'
        ]
        widgets = {
            'order': forms.Select(),
            'service': forms.Select(),
            'quantity': forms.NumberInput(),
            'price': forms.NumberInput()
        }