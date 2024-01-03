from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib import messages
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
def search_query(request):
  if request.method == "GET":
    query=request.GET["q"]
    
    if query:
    #  products=Product.objects.all()
     product=Product.objects.filter(title__icontains=query)
    #  if query not in product:
    #    messages.error(request,"NO RESULT FOUND!!!")
    #    return redirect('/')
    else:
     product=Product.objects.all()
    return render (request,'app/searched.html',{'product':product})



class CustomerRegistrationView(View):
  def get(self,request):
     form= CustomerRegistrationForm()
     return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if form .is_valid():
      messages.success(request,'congratulations!!! Registered successfully')
      form.save()
    return render(request,'app/customerregistration.html',{'form':form})
  
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount   =  0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
   for p in cart_product:
       tempamount = (p.quantity * p.product.discounted_price)
       amount += tempamount
   totalamount = amount+shipping_amount

 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})
@login_required
def add_to_cart(request):
 user = request.user
 product_id=request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

# def buy_now(request):
#  return render(request, 'app/buynow.html')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all()if p.user == user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity*p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
    else:
      return render(request,'app/emptycart.html')

class ProductView(View):
 def get(self,request):
  fertilizer = Product.objects.filter(category='F')
  insecticide = Product.objects.filter(category='I')
  pesticide = Product.objects.filter(category='P')
  manure = Product.objects.filter(category='M')
  return render(request,'app/home.html',{'fertilizer':fertilizer,'insecticide':insecticide,'pesticide':pesticide,'manure':manure})
 
class ProductDetailView(View):
  def get(self,request,pk):               
    product = Product.objects.get(pk=pk)
    share_link = request.build_absolute_uri(reverse('product-detail', args=[pk]))
    item_already_in_cart = False
    if request.user.is_authenticated:
       item_already_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
    return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'share_link':share_link})
  
def fertilizer(request,data=None):
  if data == None:
    fert = Product.objects.filter(category = 'F')
  elif data =='below':
    fert = Product.objects.filter(category='F').filter(discounted_price__lt =500)
  elif data =='above':
    fert= Product.objects.filter(category='F').filter(discounted_price__gt =500)
  # elif data =='Nitrogen Fertilizer' or data =='Phosphorous Fertilizer' or data == 'Zinc Fertilizer':
  #   fert= Product.objects.filter(category='F').filter(title=data)
  return render(request, 'app/fertilizer.html',{'fert':fert})

  
def insecticide(request,data=None):
  if data == None:
    insect = Product.objects.filter(category = 'I')
  elif data =='below':
    insect = Product.objects.filter(category='I').filter(discounted_price__lt =500)
  elif data =='above':
    insect= Product.objects.filter(category='I').filter(discounted_price__gt =500)
  # elif data =='Nitrogen Fertilizer' or data =='Phosphorous Fertilizer' or data == 'Zinc Fertilizer':
  #   fert= Product.objects.filter(category='F').filter(title=data)
  return render(request, 'app/insecticide.html',{'insect':insect})

def pesticide(request,data=None):
  if data == None:
    pest = Product.objects.filter(category = 'P')
  elif data =='below':
    pest = Product.objects.filter(category='P').filter(discounted_price__lt =500)
  elif data =='above':
    pest= Product.objects.filter(category='P').filter(discounted_price__gt =500)
  # elif data =='Nitrogen Fertilizer' or data =='Phosphorous Fertilizer' or data == 'Zinc Fertilizer':
  #   fert= Product.objects.filter(category='F').filter(title=data)
  return render(request, 'app/pesticide.html',{'pest':pest})


def manure(request,data=None):
  if data == None:
    manure = Product.objects.filter(category = 'M')
  elif data =='below':
    manure = Product.objects.filter(category='M').filter(discounted_price__lt =500)
  elif data =='above':
    manure= Product.objects.filter(category='M').filter(discounted_price__gt =500)
  # elif data =='Nitrogen Fertilizer' or data =='Phosphorous Fertilizer' or data == 'Zinc Fertilizer':
  #   fert= Product.objects.filter(category='F').filter(title=data)
  return render(request, 'app/manure.html',{'manure':manure})


@login_required
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request,'app/address.html',{'add':add,'active':'btn-primary'})


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'congratulations!! profile updated successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.quantity += 1
    c.save()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
      
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.quantity -= 1
    c.save()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
       
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data) 
  
@login_required  
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

  
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.delete()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
      
    data = {
    
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data) 
  
@login_required
def orders(request):
   op = OrderPlaced.objects.filter(user=request.user)
   return render(request,'app/orders.html',{'order_placed':op})
  


      
