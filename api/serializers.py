from rest_framework import serializers
from storeapp.models import *


##*********************************************************************************************##

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug']
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.UUIDField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given id was found.')
        return value
    
    def save(self, **kwargs):
        cart_id =self.context['cart_id']
        product_id =self.validated_data['product_id']
        quantity =self.validated_data['quantity']
        
        try:
            cartitem=Cartitems.objects.get(cart_id=cart_id,product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance=cartitem
        except :
            self.instance=Cartitems.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    
    
    class Meta:
        model=Cartitems
        fields=['id','product_id','quantity']
        
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cartitems
        fields=['quantity']
    
class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=120000,allow_empty_file=False,use_url=False),
        write_only=True
    )
    class Meta:
        model = Product
        fields = ['id', 'name', 'description','price','images','uploaded_images']
        
    def create(self, validated_data):
        uploaded_images=validated_data.pop('uploaded_images')
        product=Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product,image=image)
        return product
        
    
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
    items=CartItemSerializer(many=True,read_only=True)
    grand_total=serializers.SerializerMethodField(method_name='main_total')
    class Meta:
        model=Cart
        fields=['cart_id','items','grand_total']
        
    def main_total(self,cart:Cart):
        items = cart.items.all()
        return sum([item.quantity * item.product.price for item in items])
    

##***************************************************************************************##

