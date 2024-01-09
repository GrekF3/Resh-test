# payments/urls.py

from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexPageView.as_view(), name='home'),
    path('config/', views.stripe_config),
    path('buy/<int:id>/', views.create_checkout_session),
    path('item/<int:id>/', views.product_view),
    path('success/', views.SuccessView.as_view()), 
    path('cancelled/', views.CancelledView.as_view()), 
    path('order/<int:id>/', views.order_view),
    path('create_order_session/<int:id>/', views.create_order_session),
]