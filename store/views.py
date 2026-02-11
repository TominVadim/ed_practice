from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView
from .models import Product, Order, Supplier
from .filters import ProductFilter
from .forms import ProductAdminForm

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in self.allowed_roles

class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 15
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category', 'manufacturer', 'supplier')
        if self.request.user.is_authenticated and self.request.user.role == 'guest':
            qs = qs[:50]
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        return context

class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Product
    form_class = ProductAdminForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')
    allowed_roles = ['admin']
    
    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно добавлен')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Product
    form_class = ProductAdminForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')
    allowed_roles = ['admin']

class ProductDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    allowed_roles = ['admin']
    template_name = 'store/product_confirm_delete.html'
    
    def form_valid(self, form):
        if self.object.order_items.exists():
            messages.error(self.request, 'Нельзя удалить товар, который есть в заказах')
            return redirect('product_list')
        messages.success(self.request, 'Товар удален')
        return super().form_valid(form)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('user', 'pickup_point').prefetch_related('items__product')
        if self.request.user.role == 'client':
            qs = qs.filter(user=self.request.user)
        return qs
