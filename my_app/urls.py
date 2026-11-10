from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileView, CategoryListAPIView, CategoryDetailAPIView,
                     SubCategoryListAPIView, SubCategoryDetailAPIView,ProductListAPIView,
                    ProductDetailAPIView,CartViewSet, CartItemViewSet,
                    ReviewViewSet, RegisterView, LoginView, LogoutView)

router = routers.SimpleRouter()

router.register(r'user', UserProfileView)
router.register(r'review', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('sub_category/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('cart/', CartViewSet.as_view(), name='cart_detail'),
    path('cart_items/', CartItemViewSet.as_view({'get':'list', 'post':'create'})),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put':'update', 'delete':'destroy'})),
]