from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# class User(models.Model):
#     name = models.CharField(unique=True, max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     created_at = models.DateField()
#     role = models.CharField(max_length=255)
    
class User(AbstractUser):
    # Пользователь с определенной ролью (сотрудний, клиент, админ и т.д.)
    role = models.CharField(max_length=55, blank=True)    

class TypeOfPet(models.Model): 
    # Тип питомца (собака, кошка, рыба и т.д.)
    name = models.CharField(max_length=255, unique=True)

class Breed(models.Model):
    # порода питомца
    type_of_pet = models.ForeignKey(TypeOfPet, on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(max_length=255)
    
class Pet(models.Model):
    # питомец
    name = models.CharField(max_length=255)
    type_of_pet = models.ForeignKey(TypeOfPet, on_delete=models.CASCADE, related_name='pets')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='pets')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    birth_date = models.DateField()
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='pets')
    

class Order(models.Model):
    # Заказ клиента
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)

class Service(models.Model): 
    # услуга, предоставлемая питомцу клиента (осмотр, анализы и т.д.)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveBigIntegerField(default=0)

class OrderService(models.Model):
    # Услуга, входящяя в заказ. Содержит id заказа и id услуги
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='order_services')
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ServiceTypeOfPet(models.Model):
    # Тип питомца (собака, кошка, птица и т.д.), которому может быть оказана определенная услуга
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='services_type_of_pet')
    type_of_pet = models.ForeignKey(TypeOfPet, on_delete=models.CASCADE, related_name='services_type_of_pet') 
    