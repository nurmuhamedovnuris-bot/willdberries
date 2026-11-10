from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import TextField
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
  STATUS_CHOICES = (
      ('gold', 'gold'),
      ('silver', 'silver'),
      ('bronze', 'bronze'),
      ('simple', 'simple'),
  )

  age = models.PositiveSmallIntegerField( validators=[MinValueValidator(16), MaxValueValidator(70)],null=True, blank=True,)
  phone_number = PhoneNumberField(region='KG', blank=True, null=True)
  status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='simple')
  date_register = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    category_name= models.CharField(max_length=32, unique= True)
    category_image=models.ImageField(upload_to='photo_category/')

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    subcategory_name=models.CharField(max_length=32, unique=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    price=models.PositiveSmallIntegerField()
    descriptions=models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product_sub')
    type=models.BooleanField()
    article=models.PositiveIntegerField(unique=True)
    video=models.FileField(null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.price} {self.product_name}'

    def get_average_rating(self):
        ratings = self.review_product.all()
        if ratings.exists():
            return sum(i.star for i in ratings) / ratings.count()
        return 0

    def get_count_people(self):
        ratings = self.review_product.all()
        if ratings.exists():
            return ratings.count()
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photo_product')
    product_image = models.ImageField(upload_to="image_product/")

    def __str__(self):
        return self.product.product_name


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    star= models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                           null=True, blank=True)
    text= models.TextField( null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.product_name} {self.star}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product} {self.quantity}'

    def get_total_price(self):
        return self.quantity * self.product.price