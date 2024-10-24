from django.contrib import admin # type: ignore

from multishop.models import Brand, Cart, CartItem, Category, Color, Product, Size, Slider, Tag

# Register your models here.
admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Cart)
admin.site.register(CartItem)
#admin.site.register()
#admin.site.register()
#admin.site.register()