import django_filters
from django.db.models import Q
from .models import Product, Supplier

class ProductFilter(django_filters.FilterSet):
    supplier = django_filters.ChoiceFilter(
        field_name='supplier__name',
        label='Поставщик',
        empty_label='Все поставщики'
    )
    
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск'
    )
    
    sort = django_filters.OrderingFilter(
        fields=(
            ('stock_quantity', 'quantity'),
        ),
        field_labels={
            'stock_quantity': 'По количеству на складе',
        }
    )
    
    class Meta:
        model = Product
        fields = ['supplier', 'search']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(article__icontains=value) |
            Q(description__icontains=value)
        )
