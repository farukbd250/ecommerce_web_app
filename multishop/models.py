from django.db import models # type: ignore
from django.utils.text import slugify # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.contrib.auth.models import User
# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slider_images/')
    link = models.URLField(blank=True)
    
    
    def __str__(self):
        return self.title
    # Category Data Model
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cate_image = models.ImageField(upload_to='mohter-category/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    # Brand Data Model
class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=5)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Product model for storing fashion products
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    product_type = models.CharField(max_length=50, choices=[('Featured', 'Featured'), ('Regular', 'Regular'), ('Up Comming', 'Up Comming')], default='Regular')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    size = models.ManyToManyField('Size', blank=True)
    color = models.ManyToManyField('Color', blank=True)
    description = models.TextField()
    price = models.IntegerField()
    discount_percentage = models.IntegerField(default=0)
    discount_price = models.FloatField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    image_back = models.ImageField(upload_to='products/', blank=True)
    image_side = models.ImageField(upload_to='products/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def save(self, *args, **kwargs):
        # Validate discount_percent
        if not (0 <= self.discount_percentage <= 100):
            raise ValidationError("Discount percent must be between 0 and 100.")

        # Calculate discount_price if discount_percent is provided
        if self.discount_percentage > 0:
            self.discount_price = self.price * (1 - (self.discount_percentage / 100))
        else:
            self.discount_price = None  # or set it to self.price if no discount is applied

        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # Data model for Cart 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return  f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.discount_price if self.product.discount_price else self.product.price * self.quantity
    