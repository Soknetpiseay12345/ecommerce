from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse
from .models import ShoppingCart, CartItem, Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login after successful signup
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserCreationForm()

    return render(request, 'store/signup.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    if request.headers.get('Accept') == 'application/json':
        product_data = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
        return JsonResponse({'products': product_data}, status=200)
    return render(request, 'store/product_list.html', {'products': products})


def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# @csrf_exempt
# @login_required
# def add_to_cart(request, product_id):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, id=product_id)
#         cart, created = ShoppingCart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()

#         # Respond with a success message
#         return JsonResponse({'message': 'Product added to cart!'})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@login_required
def add_to_cart(request):
    print(f"User: {request.user}") 
    if not request.user.is_authenticated:  
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            body_data = json.loads(request.body)
            product_id = body_data.get('productId', None)

            if not product_id:
                return JsonResponse({'error': 'Product ID is missing'}, status=400)

            # Get the product and the user's shopping cart
            product = Product.objects.get(id=product_id)
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)

            # Add the product to the cart (or increase quantity if it already exists)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if created:  # If the item is newly created, set the quantity to 1
                cart_item.quantity = 1
            else:  # If the item already exists, increase the quantity
                cart_item.quantity += 1
            
            cart_item.save()

            return JsonResponse({'success': 'Product added to cart successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

 
@login_required
def cart_view(request):
    try:
        # Get the shopping cart for the authenticated user
        cart = ShoppingCart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Save cart_id in session
        request.session['cart_id'] = cart.id

        # If there are no cart items, pass a flag or message
        if not cart_items:
            cart_empty = True
        else:
            cart_empty = False
            # Add item_total for each cart item
            for item in cart_items:
                item.item_total = item.product.price * item.quantity

        return render(request, 'store/cart_view.html', {'cart_items': cart_items, 'cart_empty': cart_empty})

    except ShoppingCart.DoesNotExist:
        # If no cart exists for the user, you can still return an empty cart
        return render(request, 'store/cart_view.html', {'cart_items': [], 'cart_empty': True})

@csrf_exempt
@login_required
def update_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            product_id = data.get('product_id')
            cart = ShoppingCart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

            # Update the cart item based on the action
            if action == 'increase':
                if cart_item.product.stock > cart_item.quantity:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    return JsonResponse({'error': 'Not enough stock available.'})

            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

            elif action == 'remove':
                cart_item.delete()

            # Recalculate the total price and item totals
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            updated_cart_items = []
            for item in cart_items:
                item_total = item.product.price * item.quantity
                updated_cart_items.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'product_price': item.product.price,
                    'quantity': item.quantity,
                    'item_total': item_total,
                })

            return JsonResponse({
                'success': 'Cart updated successfully.',
                'total_price': total_price,
                'cart_items': updated_cart_items,
            })

        except (CartItem.DoesNotExist, ShoppingCart.DoesNotExist):
            return JsonResponse({'error': 'Cart or product not found.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        # Get cart_id from session
        cart_id = request.session.get('cart_id')

        if not cart_id:
            return JsonResponse({'error': 'Cart not found'})

        try:
            cart = ShoppingCart.objects.get(id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items:
                return JsonResponse({'error': 'Your cart is empty!'})

            grand_total = 0

            # Loop through the cart items and update the product quantities in the database
            for item in cart_items:
                try:
                    product = item.product  # Access the product directly from the cart item
                    if product.stock >= item.quantity:  # Check if enough stock is available
                        product.stock -= item.quantity  # Deduct the quantity
                        product.save()  # Save the updated product
                        grand_total += product.price * item.quantity
                    else:
                        return JsonResponse({'error': f'Not enough stock for {product.name}'})
                except Product.DoesNotExist:
                    return JsonResponse({'error': 'Product not found'})

            # Clear the cart after successful checkout
            request.session['cart_id'] = None

            # Send a success response back to the frontend
            return JsonResponse({'success': f'Your purchase was successful! Total: ${grand_total:.2f}'})

        except ShoppingCart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found in the database.'})

    else:
        return JsonResponse({'error': 'Invalid request method.'})


def cart_json(request):
    try:
        cart = ShoppingCart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_empty = not cart_items
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        cart_items_data = [{
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_price': item.product.price,
            'quantity': item.quantity,
            'item_total': item.product.price * item.quantity
        } for item in cart_items]

        return JsonResponse({
            'cart_empty': cart_empty,
            'cart_items': cart_items_data,
            'total_price': total_price
        })

    except ShoppingCart.DoesNotExist:
        return JsonResponse({'cart_empty': True, 'cart_items': [], 'total_price': 0.0})
    
