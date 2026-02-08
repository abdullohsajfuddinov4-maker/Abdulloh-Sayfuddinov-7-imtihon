from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartAddSerializer, CartRemoveSerializer, CartUpdateSerializer

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product = Product.objects.filter(id=product_id).first()

        if not product:
            return Response({"error": "Product mavjud emas"}, status=status.HTTP_404_NOT_FOUND)

        cart = get_or_create_cart(request.user)

        item,created = CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            item.quantity += quantity
            item.save()
            return Response({"message": "Product cartda mavjud",'data':serializer.data}, status=status.HTTP_200_OK)
        item.quantity = quantity
        item.save()
        return Response({"message": "Product cart qo'shildi",'data':serializer.data}, status=status.HTTP_201_CREATED)

class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        cart = get_or_create_cart(request.user)
        deleted_count, _ = CartItem.objects.filter(cart=cart,product_id=product_id).delete()
        if deleted_count == 0:
            return Response({"error": "Product cartda mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Product cartdan o'chirildi"}, status=status.HTTP_200_OK)


class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({"message": "Cart bo'shatildi"}, status=status.HTTP_200_OK)


class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        cart = get_or_create_cart(request.user)
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not item:
            return Response({"detail": "Product cartda mavjud emas"}, status=status.HTTP_404_NOT_FOUND)

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)