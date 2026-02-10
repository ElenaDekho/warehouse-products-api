from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов: только id, название и описание"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции товара на складе (связующая таблица)"""
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада с вложенными позициями товаров"""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        """Создание склада с одновременным созданием связанных позиций товаров"""
        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        """Обновление склада и позиций товаров (существующие обновляются, новые добавляются)"""
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={'quantity': position['quantity'], 'price': position['price']}
            )

        return stock
