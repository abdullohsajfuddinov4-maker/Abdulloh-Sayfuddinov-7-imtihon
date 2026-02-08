from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=12, decimal_places=2, read_only=True)
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_title", "product_price", "quantity", "item_total"]

    def get_item_total(self, obj):
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ("id", "items", "total_items", "total_price")

    def get_total_price(self, obj):
        return sum((i.product.price * i.quantity) for i in obj.items.all())

    def get_total_items(self, obj):
        return sum(i.quantity for i in obj.items.all())


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False, min_value=1, default=1)


class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)