from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.db.models import Q


class StandardResultsSetPagination(PageNumberPagination):
    """Кастомная пагинация: 3 элемента на страницу, можно изменить через page_size"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductFilter(FilterSet):
    """Фильтр для продуктов с регистронезависимым поиском по названию и описанию"""
    search = CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Product
        fields = []

    def filter_search(self, queryset, name, value):
        """Поиск с использованием iregex для работы с SQLite (регистронезависимый)"""
        return queryset.filter(
            Q(title__iregex=value) | Q(description__iregex=value)
        )


class ProductViewSet(ModelViewSet):
    """ViewSet для продуктов: CRUD + поиск + пагинация"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = StandardResultsSetPagination


class StockFilter(FilterSet):
    """Фильтр для складов с возможностью:
       1) фильтрации по id продукта (?products=...)
       2) поиска по названию/описанию продукта (?search=...)"""
    search = CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Stock
        fields = ['products']   # фильтрация по id продукта

    def filter_search(self, queryset, name, value):
        """Поиск складов, где есть продукт с указанным названием или описанием"""
        return queryset.filter(
            Q(products__title__iregex=value) |
            Q(products__description__iregex=value)
        ).distinct()        # чтобы избежать дублирования складов


class StockViewSet(ModelViewSet):
    """ViewSet для складов: CRUD + фильтрация по продуктам + поиск по продуктам + пагинация"""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter  # ← меняем эту строку
    pagination_class = StandardResultsSetPagination
