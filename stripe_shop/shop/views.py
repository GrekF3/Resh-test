# payments/views.py

from django.conf import settings 
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.views.generic.base import TemplateView
import stripe
from .models import Item, Order
import json

from django.http import Http404

## Базовая страница
class IndexPageView(TemplateView):
    template_name = 'index.html'

## Конфигурация stripe для клиента
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
## Просмотра продукта
def product_view(request, id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=id)
        except Item.DoesNotExist:
            raise Http404
        context = {
            'item':item
        }
        print(item)
        return render(request,'product_detail.html',context=context)

def order_view(request,id):
    if request.method == 'GET':
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            raise Http404
        context = {
            'order':order
        }
        return render(request,'order_detail.html', context=context)

## Калькулятор всего заказа
def calculate_order_amount(order):
    items = []
    for item in order.items.all():
        items.append(int(item.price))
    return sum(items) * 100

## Сеанс оплаты заказа
@csrf_exempt
def create_order_session(request, id):
    order = get_object_or_404(Order, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Получение данных из POST запроса
        payload = request.body.decode('utf-8')
        data = json.loads(payload)
        print(data)

        # Создание PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(order),
            currency=order.currency,
            automatic_payment_methods={"enabled": True},
        )

        # Возвращаем клиентский идентификатор сессии
        return JsonResponse({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        # Обработка ошибок Stripe
        return JsonResponse({'error': str(e)}, status=400)

# Сеанс оплаты товара
@csrf_exempt
def create_checkout_session(request, id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=id)
            print(item.price * 100)
        except Item.DoesNotExist:
            raise Http404()
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                    "price_data": {
                        "currency": f"{item.currency}",
                        "product_data": {"name": f"{item}"},
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                    },
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

## Успешная оплата
class SuccessView(TemplateView):
    template_name = 'success.html'

## Отмена оплаты
class CancelledView(TemplateView):
    template_name = 'cancelled.html'