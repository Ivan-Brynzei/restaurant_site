from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Dish, Category
from django.conf import settings


def home_view(request):
    return render(request, 'menu/home.html')


def add_to_cart_ajax(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        dish_id = request.POST.get('dish_id')
        if dish_id:
            cart = request.session.get('cart', {})
            cart[dish_id] = cart.get(dish_id, 0) + 1
            request.session['cart'] = cart
            return JsonResponse({'success': True, 'quantity': cart[dish_id]})
    return JsonResponse({'success': False}, status=400)

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        subtotal = dish.price * quantity
        items.append({'dish': dish, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'menu/cart.html', {'items': items, 'total': total})

def update_cart(request):
    if request.method == 'POST':
        cart = {}
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                dish_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[dish_id] = quantity
                except ValueError:
                    continue
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        items = []
        total = 0
        for dish_id, quantity in cart.items():
            dish = get_object_or_404(Dish, id=dish_id)
            subtotal = dish.price * quantity
            total += subtotal
            items.append(f"{dish.name} x{quantity} — {subtotal:.2f} грн")

        message = (
            f"Нове замовлення:\n"
            f"ПІБ: {name}\n"
            f"Телефон: {phone}\n"
            f"Адреса: {address}\n\n" +
            "\n".join(items) +
            f"\nЗагальна сума: {total:.2f} грн"
        )

        send_mail(
            'Нове замовлення',
            message,
            'noreply@example.com',
            [settings.ADMIN_EMAIL],
        )

        del request.session['cart']
        return render(request, 'menu/checkout_success.html', {'total': total})

    return redirect('cart')
        
        
    
    
    
    
    
    
    
    

def menu_view(request):
    dishes = Dish.objects.select_related('category').all()
    categories = Category.objects.all()

    # Отримуємо GET-параметри
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by')

    # Фільтрація
    if category_id:
        dishes = dishes.filter(category_id=category_id)

    if min_price:
        dishes = dishes.filter(price__gte=min_price)

    if max_price:
        dishes = dishes.filter(price__lte=max_price)

    # Сортування
    if sort_by == 'price_asc':
        dishes = dishes.order_by('price')
    elif sort_by == 'price_desc':
        dishes = dishes.order_by('-price')

    context = {
        'dishes': dishes,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'menu/menu.html', context)
