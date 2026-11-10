from rest_framework import serializers
from .models import UserProfile, Category, SubCategory, Product, ProductImage, Review, Cart, CartItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']


class SubCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_category=SubCategoryNameSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['category_name','sub_category']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']


class ProductListSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'subcategory',
                  'photo_product', 'average_rating', 'get_count_people']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class SubCategoryListSerializer(serializers.ModelSerializer):
    category=CategoryNameSerializer()
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'category']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category=CategoryNameSerializer()
    product_sub=ProductListSerializer(read_only=True, many=True)
    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'category', 'product_sub']


class ReviewProductSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y'))
    user =UserProfileNameSerializer()
    class Meta:
        model = Review
        fields = ('id','user', 'product','text', 'star', 'created_date')


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryNameSerializer()
    photo_product=ProductImageSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(format('%d-%m-%Y'))
    review_product = ReviewProductSerializer(many=True , read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['product_name', 'article', 'descriptions',
                  'price', 'created_date', 'video', 'type',
                  'photo_product', 'subcategory', 'review_product', 'count_people', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y'))
    user =UserProfileNameSerializer()
    product = ProductListSerializer()
    class Meta:
        model = Review
        fields = ('id', 'user','text', 'star','product', 'created_date')


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product',
                                                    queryset=Product.objects.all(), write_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
