from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

JOB_TYPE = (
    ('Contract', 'Contract'),
    ('Permanent', 'Permanent'),
    ('Freelance', 'Freelancer'),
)


class Customer(models.Model):
	user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Category(models.Model):
	title = models.CharField(max_length=100)
	company_name = models.CharField(max_length=200, blank=True, null=True)
	employment_status = models.CharField(choices=JOB_TYPE, max_length=10, blank=True, null=True)
	vacancy = models.CharField(max_length=10, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	responsibilities = models.TextField(blank=True, null=True)
	experience = models.CharField(max_length=100, blank=True, null=True)
	job_location = models.CharField(max_length=120, blank=True, null=True)
	province = models.CharField(blank=True, null=True, max_length=120)
	Salary = models.CharField(max_length=100, blank=True, null=True)
	image = models.ImageField(null=True, blank=True)
	application_deadline = models.DateTimeField(blank=True, null=True)
	published_on = models.DateTimeField(blank=True, null=True)

	# status = models.CharField(blank=True, null=True, max_length=120)

	def __str__(self):
	    return self.title

	@property
	def imageURL(self):
	    try:
	        url = self.image.url
	    except:
	        url = ''
	    return url

	def get_absolute_url(self):
	    return reverse("store:single", args=[self.id])

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	# new_product = models.BooleanField(default=False,null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Distributions(models.Model):
	name = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=100)
	company_name = models.CharField(max_length=200, blank=True, null=True)
	email_adress = models.EmailField(max_length=50, blank=True, null=True)
	contact_numbers = models.CharField(max_length=12, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()
	description = models.TextField(blank=True, null=True)
	address = models.CharField(max_length=200, null=False)
	province = models.CharField(blank=True, null=True, max_length=120)
	city = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)

	# status = models.CharField(blank=True, null=True, max_length=120)

	def __str__(self):
	    return self.title

	@property
	def imageURL(self):
	    try:
	        url = self.image.url
	    except:
	        url = ''
	    return url

	def get_absolute_url(self):
	    return reverse("jobs:distributorsform", args=[self.id])