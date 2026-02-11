from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Гость'),
        ('client', 'Авторизованный клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    full_name = models.CharField('ФИО', max_length=255)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='client')
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.username

class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField('Производитель', max_length=100, unique=True)
    
    class Meta:
        db_table = 'manufacturers'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField('Поставщик', max_length=100, unique=True)
    
    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    article = models.CharField('Артикул', max_length=20, unique=True)
    name = models.CharField('Наименование', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField('Скидка %', default=0)
    stock_quantity = models.IntegerField('Количество на складе', default=0)
    description = models.TextField('Описание', blank=True)
    image_path = models.CharField('Путь к фото', max_length=500, blank=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.article} - {self.name}'
    
    def final_price(self):
        return self.price * (100 - self.discount_percent) / 100
    
    def need_highlight(self):
        return self.discount_percent > 15 or self.stock_quantity == 0

class PickupPoint(models.Model):
    address = models.CharField('Адрес', max_length=500, unique=True)
    
    class Meta:
        db_table = 'pickup_points'
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'
    
    def __str__(self):
        return self.address

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='managed_orders', verbose_name='Менеджер')
    order_date = models.DateField('Дата заказа')
    delivery_date = models.DateField('Дата доставки', null=True, blank=True)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, verbose_name='Пункт выдачи')
    receive_code = models.CharField('Код получения', max_length=10)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']
    
    def __str__(self):
        return f'Заказ №{self.order_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.IntegerField('Количество')
    price_at_order = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
