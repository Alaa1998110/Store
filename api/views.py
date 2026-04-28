from rest_framework.decorators import api_view
from rest_framework.response import Response    
from storeapp.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filter import *
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination  
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['old_price']
    pagination_class = PageNumberPagination
    
    
class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class=CartSerializer
    queryset=Cart.objects.all()
    

class CartItemViewSet(ModelViewSet):
    # serializer_class=CartItemSerializer
    
    http_method_names=['get','post','patch','delete']   
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
       
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])
    
    
# class ApiProducts(ListCreateAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
    
# class Api_product(RetrieveUpdateDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
    
    
# class Api_categories(ListCreateAPIView):
#     queryset=Category.objects.all()
#     serializer_class=CategorySerializer
    

# class Api_category(RetrieveUpdateDestroyAPIView):
#     queryset=Category.objects.all()
#     serializer_class=CategorySerializer

# class ApiProducts(APIView):
#     def get(self,request):
#       products=Product.objects.all()
#       serializer=ProductSerializer(products,many=True)
#       return Response(serializer.data)
#     def post(self,request):
#       serializer=ProductSerializer(data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
    



# @api_view(['GET', 'POST'])
# def api_products(request):
#     if request.method == 'GET':
#       products=Product.objects.all()
#       seializer=ProductSerializer(products,many=True)
#       return Response(seializer.data)
#     elif request.method == 'POST':
#       serializer=ProductSerializer(data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
  
    
# class Api_product(APIView):
#     def get(self,request,pk):
#       product=get_object_or_404(Product,id=pk)
#       serializer=ProductSerializer(product)
#       return Response(serializer.data)
#     def put(self,request,pk):
#       product=get_object_or_404(Product,id=pk)
#       serializer=ProductSerializer(product,data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#     def delete(self,request,pk):
#       product=get_object_or_404(Product,id=pk)
#       product.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def api_product(request,pk):
#     product=get_object_or_404(Product, id=pk)
#     if request.method=='GET':
#       serializer=ProductSerializer(product)
#       return Response(serializer.data)
#     elif request.method=='PUT':
#       serializer=ProductSerializer(product,data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#     elif request.method=='DELETE':
#       product.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)

# class Api_categories(APIView):
#     def get(self,request):
#       categories=Category.objects.all()
#       serializer=CategorySerializer(categories,many=True)
#       return Response(serializer.data)
#     def post(self,request):
#       serializer=CategorySerializer(data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
# @api_view(['GET', 'POST'])
# def api_categories(request):
#     if request.method == 'GET':
#       categories=Category.objects.all()
#       serializer=CategorySerializer(categories,many=True)
#       return Response(serializer.data)
#     elif request.method == 'POST':
#       serializer=CategorySerializer(data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)

# class Api_category(APIView):
#     def get(self,request,pk):
#       category=get_object_or_404(Category, category_id=pk)
#       serializer=CategorySerializer(category)
#       return Response(serializer.data)
#     def put(self,request,pk):
#       category=get_object_or_404(Category, category_id=pk)
#       serializer=CategorySerializer(category,data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#     def delete(self,request,pk):
#       category=get_object_or_404(Category, category_id=pk)
#       category.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['GET', 'PUT', 'DELETE'])
# def api_category(request,pk):
#     category=get_object_or_404(Category, category_id=pk)
#     if request.method == 'GET':
#       serializer=CategorySerializer(category)
#       return Response(serializer.data)
#     elif request.method == 'PUT':
#       serializer=CategorySerializer(category, data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#     elif request.method == 'DELETE':
#       category.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)





    