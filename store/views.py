from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .forms import *
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	categories = Category.objects.all()
	print(categories)
	context = {'products':products, 'cartItems':cartItems, 'categories':categories}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)



def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

# from.django.views.decorators.csrf import csrf_exempt	

# @csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

# @login_required
def seller_post(request):

    form = SellerListingForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/store/seller-post/')
    context = {
        'form': form,

    }
    return render(request, "store/seller-post.html", context)

def contact(request):
	context = {
	    'form': "form",

	}
	return render(request, "store/contact.html", context)

# def about_us(request):
# 	context = {}
# 	return render(request, "store/about-us.html", context)

def about(request):
	context = {
	    'form': "form",

	}
	return render(request, "store/about.html", context)

def aboutpricing(request):
	qs = Category.objects.all().order_by('-published_on')
	jobs = Category.objects.all().count()
	user = User.objects.all().count()
	company_name = Category.objects.filter(company_name__startswith='P').count()
	paginator = Paginator(qs, 5)  # Show 5 jobs per page
	page = request.GET.get('page')
	try:
	    qs = paginator.page(page)
	except PageNotAnInteger:
	    qs = paginator.page(1)
	except EmptyPage:
	    qs = paginator.page(paginator.num_pages)

	context = {
	    'query': qs,
	    'job_qs': jobs,
	    'company_name': company_name,
	    'candidates': user
	}
	return render(request, "store/pricing.html", context)

def aboutsingle(request,  id):
	job_query =  get_object_or_404(Category, id=id)

	context = {'q': job_query,}
	return render(request, "store/single.html", context)

def services(request):
	context = {}
	return render(request, "store/services.html", context)

	

def aboutlive(request):
	context = {}
	return render(request, "store/about_live.html", context)

def aboutportion(request):
	context = {}
	return render(request, "store/about_portion.html", context)

def aboutslaughtered(request):
	context = {}
	return render(request, "store/about_slaughtered.html", context)

def abouttransport(request):
	context = {}
	return render(request, "store/about_transport.html", context)

def distributorspost(request):
	context = {}
	return render(request, "store/distributors.html", context)


def distributorsform(request):

    form = DistributionsForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/store/distributorsform/')
    context = {
        'form': form,

    }
    return render(request, "store/distributors-form.html", context)					