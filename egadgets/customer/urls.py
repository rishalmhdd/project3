from django.urls import path
from .views import *




urlpatterns=[
    path('chome',CustomerHomeView.as_view(),name='home'),
    path('plist/<str:cat>',ProductListView.as_view(),name='plist'),
    path('pdetail/<int:pid>',ProductDetailsView.as_view(),name='pdetail'),
    path('cart/<int:id>',addToCart,name='acart'),
    path('cartlist',CartListView.as_view(),name='cartlist'),
    path('inc/<int:id>',increaseQuantity,name='incQuantity'),
    path('dnc/<int:id>',decreaseQuantity,name='dncQuantity'),
    path('delete/<int:id>',deleteCartItem,name='deleteCart'),
    path('placeord/<int:id>',PlaceOrderView,name='order'),
    path('ordrlsit',OrderPlaceView.as_view(),name='orders'),
    path('ocancel/<int:id>',cancelOrder,name='ordercancel'),
    path('search',searchProduct,name='search'),
    
    


]