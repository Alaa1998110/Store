from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('categories',views.CategoryViewSet)
router.register('carts',views.CartViewSet)

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

#nested router for cart items
cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart-items')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
]




# urlpatterns = [
# path('products/', views.ApiProducts.as_view(), name='api_products'),
# #we used str for pk as uuid is string not integer
# path('products/<str:pk>/', views.Api_product.as_view(), name='api_product'),
# path('categories/', views.Api_categories.as_view, name='api_categories'),
# path('categories/<str:pk>/', views.Api_category.as_view(), name='api_category'),  
# ]