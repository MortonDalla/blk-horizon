from django.urls import path

from . import views
app_name = 'store'
urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('seller-post/', views.seller_post, name='seller-post'),
	path('contact/', views.contact, name='contact'),
	# path('about-us/', views.about_us, name='about-us'),
	path('about/', views.about, name='about'),

	path('pricing/', views.aboutpricing, name='pricing'),
	path('single/<int:id>/', views.aboutsingle, name='single'),
	path('services/', views.services, name='services'),
	
	path('about_live/', views.aboutlive, name='about_live'),
	path('about_portion/', views.aboutportion, name='about_portion'),
	path('about_slaughtered/', views.aboutslaughtered, name='about_slaughtered'),
	path('about_transport/', views.abouttransport, name='about_transport'),
	path('distributors/', views.distributorspost, name='distributors'),
	path('distributorsform/', views.distributorsform, name='distributorsform'),

]