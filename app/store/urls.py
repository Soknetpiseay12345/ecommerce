from django.urls import path
from .views import checkout, login_view, signup_view , product_list , add_to_cart , cart_view , logout_view , update_cart , cart_json

urlpatterns = [
    path('accounts/login/',login_view , name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('', product_list, name='home'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/', update_cart , name= 'update_cart'  ),
    path('cart_json/', cart_json , name= 'cart_json'  )
    
]
