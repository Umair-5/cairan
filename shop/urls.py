
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product, name='product'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
