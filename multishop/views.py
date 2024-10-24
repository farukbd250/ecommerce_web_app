from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import redirect, render  # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from django.contrib.auth.models import User # User Data Model base import here to register
from django.contrib.auth import authenticate, login, logout # Log in and authenticte view
from django.shortcuts import render  # type: ignore
from django.views.generic import TemplateView  # type: ignore
from multishop.models import Brand, Cart, CartItem, Category, Product, Slider
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
class RegisterView(TemplateView):
    template_name = 'multishop/register.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Access data from POST request
        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            return HttpResponse("Passwords do not match. Please try again.")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different one.")

        # Check if the email already exists
        if User.objects.filter(email=email_address).exists():
            return HttpResponse("Email address is already registered. Please use a different one.")

        # Create a new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email_address,
                password=password
            )
            user.save()

            # Redirect to another page after successful registration
            return redirect('login')  # Replace 'login' with the name of your desired URL pattern
        except Exception as e:
            return HttpResponse(f"An error occurred during registration: {str(e)}")
# Log in View
class LoginView(TemplateView):
    template_name = 'multishop/login.html' 
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Access data from POST request
        login_input = request.POST.get('login_input')  # This field can take username or email
        password = request.POST.get('password')

        # Attempt to authenticate the user using username or email
        try:
            # Check if the login_input is an email address or username
            if '@' in login_input:
                # If it's an email, try to find the user by email
                user = User.objects.filter(email=login_input).first()
            else:
                # Otherwise, assume it's a username
                user = User.objects.filter(username=login_input).first()

            # Authenticate the user
            if user:
                # Authenticate using the found user's username
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('home')  # Redirect to the desired page after login
                else:
                    return HttpResponse("Invalid credentials. Please try again.")
            else:
                return HttpResponse("User not found. Please check your username or email.")

        except Exception as e:
            return HttpResponse(f"An error occurred during login: {str(e)}")
        

class LogoutView(TemplateView):
    template_name = 'multishop/logout.html'
    def get(self, request):
        logout(request)
        return redirect('home') 
# home Page
class HomeView(TemplateView):
    template_name = 'multishop/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        context['categories'] = Category.objects.all()
        context['featured'] = Product.objects.filter(product_type='Featured').order_by('-created_at')
        context['upcoming'] = Product.objects.filter(product_type='Up Comming').order_by('-created_at')
         # Filter products created in the last 24 hours (1 day)
        last_24_hours = timezone.now() - timedelta(hours=24)
        context['recent_products'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
        context['allbrand'] = Brand.objects.all()
        #print('context')
        return context
    #Category responsive and 
class CategoryView(TemplateView):
    template_name = 'multishop/category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        context['category'] = category
        context['products'] = Product.objects.filter(category=category).order_by('-created_at')
        return context
# Brand Wise Data Filter
class BrandView(TemplateView):
    template_name = 'multishop/brand.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        brand = get_object_or_404(Brand, slug=slug)
        context['brand'] = brand
        context['brands'] = Product.objects.filter(brand=brand)
        return context
        
    
    # Shop Views all
class ShopView(TemplateView):
    template_name = 'multishop/shop.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-created_at')
        return context
    
    #Dtails Manual Error Handle 
class DetailView(TemplateView):
    template_name = 'multishop/detail_error.html'
    
    # Shop Views all
class DetailsView(TemplateView):
    template_name = 'multishop/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        item = get_object_or_404(Product, slug=slug)
        context['item'] = item
        context['details'] = Product.objects.filter(slug=slug)
         # Fetch related products by category, excluding the current product
        related_products = Product.objects.filter(category=item.category).exclude(id=item.id)[:6]
        context['related_products'] = related_products
        
        return context
    # Add to cart any items for authenticate user


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_item.quantity >= 10:
            messages.warning(request, "You have already added 10 items of this product to your cart. To add more, please complete your current order.")
            return redirect('shop')  # Redirect or stay on the same page
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    messages.success(request, "Item added to cart.")
    return redirect('shop')  # Redirect to the cart page or wherever needed



# to Removing the items from carts 
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')  # Redirect to the cart page after removing the item
    # calculate all cart items that are a user added on his cart 

class CartView(TemplateView):
    template_name = 'multishop/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            cart_items = CartItem.objects.filter(cart=cart) if cart else []
            cart_count = cart_items.count() if cart else []
            
            total_price = sum(item.total_price for item in cart_items)
            shipping_cost = 40  # Example fixed shipping cost
            total_price_with_shipping = total_price + shipping_cost
            
            context['cart_count'] = cart_count
            context['cart_items'] = cart_items
            context['total'] = total_price
            context['total_with_shipping'] = total_price_with_shipping  # Add this to the context
        else:
            context['cart_count'] = 0
            context['total'] = 0  # If not authenticated, total is 0
            context['total_with_shipping'] = 0  # If not authenticated, total with shipping is also 0
        return context
    
class CheckOutView(TemplateView):
    template_name = 'multishop/checkout.html'
    
class ContactView(TemplateView):
    template_name = 'multishop/contact.html'