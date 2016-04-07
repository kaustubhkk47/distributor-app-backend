"""distributorAppAPIs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from urlHandlers.login import distributor_login, salesman_login
from urlHandlers.user_details import retailer_details, salesman_details
from urlHandlers.catalog_details import get_offers, get_products, get_offer_types, order_offer_details, product_offer_details
from urlHandlers.order_details import order_details
from urlHandlers.tracking_details import tracking_details

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^distributor/login$', distributor_login),
    url(r'^salesman/login$', salesman_login)
]

## users related URLs
urlpatterns += [
    url(r'^users/retailers/$', retailer_details),
    url(r'^users/retailers/(\d+)', retailer_details),
    url(r'^users/salesman/$', salesman_details),
    url(r'^users/salesman/(\d+)', salesman_details)

]

## catalog related
urlpatterns += [
    url(r'^offers/$', get_offers),
    url(r'^offers/offer-types/$', get_offer_types),
    url(r'^offers/order-offer/$', order_offer_details),
    url(r'^offers/product-offer/$', product_offer_details),
    url(r'^products/$', get_products)
]

## order related
urlpatterns += [
    url(r'^orders/$', order_details)
]

##tracking
urlpatterns += [
    url(r'^tracking/$', tracking_details)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
