from rest_framework import serializers
from storeapp.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'slug', 'inventory', 'old_price','price']
        
    category=CategorySerializer()
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date_created','description','name']
        
    def create(self,validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer(many=False)
    subtotal=serializers.SerializerMethodField(method_name='total')
    class Meta:
        model=Cartitems
        fields=['id','cart','product','quantity','subtotal']
        
    def total(self,cartitem:Cartitems):
        return cartitem.quantity*cartitem.product.price
    
    
class CartSerializer(serializers.ModelSerializer):
    cart_id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True)
    class Meta:
        model=Cart
        fields=['cart_id','items']
        
