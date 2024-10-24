from multishop.models import Cart, CartItem, Category

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_count = CartItem.objects.filter(cart=cart).count() if cart else 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}