from django.urls import path # type: ignore

from multishop.views import BrandView, CartView, CategoryView, CheckOutView, ContactView, DetailView, DetailsView, HomeView, LoginView, LogoutView, RegisterView, ShopView, add_to_cart, remove_from_cart


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('brand/<slug:slug>/', BrandView.as_view(), name='brand'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('detial/', DetailView.as_view(), name='detail'),
    path('detials/<slug:slug>/', DetailsView.as_view(), name='indetail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
   # path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
   path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    #path('shop/', ShopView.as_view(), name='shop'),
]
