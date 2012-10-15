# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from shop.util.decorators import on_method, shop_login_required
from django.forms.forms import DeclarativeFieldsMetaclass
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from shop_stripe.forms import CardForm
import stripe

class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class StripeBackend(object):
    '''
    A django-shop payment backend for the stripe service, this 
    is the workhorse view. It processes what the CardForm class
    kicks back to the server.
    
    It also saves the customer billing information for later use.
    '''
    backend_name="Stripe"
    url_namespace="stripe"

    def __init__(self, shop):
        self.shop = shop
        self.key = getattr(settings, 'SHOP_STRIPE_KEY', None)
        self.currency = getattr(settings, 'SHOP_STRIPE_CURRENCY', None)

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.stripe_payment_view, name='stripe' ),
            url(r'^success/$', self.stripe_return_successful_view, name='stripe_success' ),
        )
        return urlpatterns

    def stripe_payment_view(self, request):
        if request.POST:
            if request.user.is_authenticated() and not request.user.get_profile().stripe_customer_id == '':
                customer_id = request.user.get_profile().stripe_customer_id 
            else:
                customer_id=None
                card_token = request.POST['stripeToken']
            order = self.shop.get_order(request)
            order_id = self.shop.get_order_unique_id(order)
            amount = self.shop.get_order_total(order)
            amount = str(int(amount * 100))
            if request.user.is_authenticated():
                description = request.user.email
            else:
                description = 'guest customer'
            
            currency = getattr(settings, 'SHOP_STRIPE_CURRENCY', 'usd') # Default to good ol' U.S. Dollar
            
            if hasattr(settings, 'SHOP_STRIPE_PRIVATE_KEY'):
                stripe.api_key=settings.SHOP_STRIPE_PRIVATE_KEY
            else: 
                raise ConfigError('You must set SHOP_STRIPE_PRIVATE_KEY in your configuration file.')
            
            if not customer_id:
                stripe_dict = {
                    'amount':amount,
                    'currency':currency,
                    'card':card_token,
                    'description':description,}
            else:
                stripe_dict = {
                    'amount':amount,
                    'currency':currency,
                    'customer':customer_id,
                    'description':description,}
            
            stripe_result = stripe.Charge.create(**stripe_dict)
            self.shop.confirm_payment(self.shop.get_order_for_id(order_id), amount, stripe_result['id'], self.backend_name)

            # If we're logged in, save the transaction token for use again later. Sweet.
            if request.user.is_authenticated and request.user.get_profile().stripe_customer_id == None: 
                customer = stripe.Customer.create(card=card_token, description=description)
                profile = request.user.get_profile()
                profile.stripe_customer_id = customer.id
                profile.save()
             
        if hasattr(settings, 'SHOP_STRIPE_PUBLISHABLE_KEY'):
            pub_key=settings.SHOP_STRIPE_PUBLISHABLE_KEY
        else: 
            raise ConfigError('You must set SHOP_STRIPE_PUBLISHABLE_KEY in your configuration file.')
        form = CardForm
        context = RequestContext(request, {'form':form, 'STRIPE_PUBLISHABLE_KEY':pub_key})
        return render_to_response("shop_stripe/payment.html", context)


    def stripe_return_successful_view(self, request):
        return HttpResponseRedirect(self.shop.get_finished_url())

