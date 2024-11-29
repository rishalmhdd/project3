from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from account.models import products,Cart,Orders
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.


# class CustomerHomeView(View):
#     def get(self,request):
#         return render(request,'home.html')


def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First!!")
            return redirect('logout')
    return inner    

decoraters=[never_cache,signin_required]

@method_decorator(decorator=decoraters,name='dispatch')
class  CustomerHomeView(TemplateView):
    template_name="home.html"

@method_decorator(decorator=decoraters,name='dispatch')
class ProductListView(ListView):
    template_name='productlist.html'
    queryset=products.objects.all()
    context_object_name="products"
    def get_queryset(self):
        cat=self.kwargs.get('cat')
        self.request.session['category']=cat
        return self.queryset.filter(category=cat)
    
def searchProduct(request,*args,**kwargs):
    keyword=request.POST['searchkey'] 
    cat=request.session['category']
    if keyword:
        product=products.objects.filter(title__icontains=keyword,category=cat)
        return render(request,'productlist.html',{"products":product})
    
    else:
        return redirect('plist',cat=cat)   
    
@method_decorator(decorator=decoraters,name='dispatch')    
class ProductDetailsView(DetailView):
    template_name="productdetails.html"
    queryset=products.objects.all()
    context_object_name="product"
    pk_url_kwarg="pid"    

decoraters
def addToCart(request,*args,**kwargs):
    try:
        pid=kwargs.get('id')
        product=products.objects.get(id=pid)
        user=request.user
        caertcheck= Cart.objects.filter(product=product,user=user).exists()
        if caertcheck:
            cartitem=Cart.objects.get(product=product,user=user)
            cartitem.quantity+=1
            cartitem.save()
            messages.success(request,"Cart-Item Quantity Increased")
            return redirect('home')
        else:
            Cart.objects.create(product=product,user=user)
            messages.success(request,f"{product.title} Added To Cart!! ")
            return redirect('home')
    except Exception as e:
        print(e)
        messages.warning(request,"Something went wrong")
        return redirect('home')    
   
    
@method_decorator(decorator=decoraters,name='dispatch')
class CartListView(ListView):
    template_name='cartlist.html'
    queryset=Cart.objects.all()
    context_object_name='carts'
    def get_queryset(self):
        qs=self.queryset.filter(user=self.request.user)
        return qs
    
decoraters    
def increaseQuantity(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.quantity+=1
        cart.save()
        return redirect('cartlist')
    except:
        messages.warning(request,"Something Went Wrong!!")
        return redirect('cartlist')    

decoraters        
def decreaseQuantity(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        if cart.quantity ==1: 
            cart.delete()
            return redirect('cartlist')
        else:
            cart.quantity-=1
            cart.save()
        return redirect('cartlist')
    except:
        messages.warning(request,"somehing went wrong!!")
        return redirect('cartlist')     

decoraters
def deleteCartItem(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.delete()
        messages.success(request,"Item Removed From cart!!")
        return redirect('cartlist')
    except:
        messages.warning(request,"Somthing Went wrong!!")
        return redirect('cartlist')    

decoraters
def PlaceOrderView(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)  
        Orders.objects.create(product=cart.product,user=request.user,quantity=cart.quantity)
        cart.delete()


        #mailsening
        subject="Egadgtes order Notifications"
        msg=f"Order for {cart.product.title} is placed"
        f_rom="rishalnk@gmail.com"
        to_id=request.user.email
        send_mail(subject,msg,f_rom,[to_id],fail_silently=True)


        messages.success(request,f'{cart.product.title}\'s Order placed!!')
        return redirect('cartlist')
    except:
        messages.warning(request,"Something Went Wrong!!")
        return redirect('cartlist')   
    

@method_decorator(decorator=decoraters,name='dispatch')    
class OrderPlaceView(ListView):
    template_name='orders.html'
    queryset=Orders.objects.all()
    context_object_name='orders'
    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)
    
decoraters    
def cancelOrder(request,**kwargs):
    try:
        oid=kwargs.get('id')
        order=Orders.objects.get(id=oid)
        order.status="Cancelled"
        order.save()
        messages.warning(request,"Order Cancelled!!")
        return redirect('orders')
    except:
        messages.warning(request,"Something went Wrong!!")
        return redirect('orders')


          
                      