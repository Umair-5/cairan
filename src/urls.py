from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_items/', views.get_cart_items, name='get_cart_items'),
    path('delete/<uuid:item_id>/', views.delete_item, name='delete'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('place_order/',views.place_order, name='place_order'),
    path('shop/', include('shop.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
