Django Shop Stripe plugin
============================

A plugin to use stripe with django-shop.

http://www.stripe.com

Installation
--------------

Add `shop_stripe` to your INSTALLED_APPS variable in your settings.py file.

Next, add a few configuration variables in the same file:

    SHOP_STRIPE_PUBLISHABLE_KEY='my-publishable-key'
    SHOP_STRIPE_PRIVATE_KEY='my-super-secret-private-key'
    
    SHOP_PAYMENT_BACKENDS = (
                ...
                'shop_stripe.offsite_stripe.StripeBackend',
                ...
                )

That's it!

Usage
-------

Thanks to Stripe.com's wonderful jscript features, it's painfully simple to integrate.

The shop_stripe plugin uses all the default django-shop templates, and the most important for our purposes is:

    shop_stripe/payment.html

Here's an example to handle Stripe test input:

    {% extends "base.html" %}
    
    {% block extra-head %}
    {% include "_stripe_head.html" %}
    {% endblock %}
    
    {% block content %}
      <h2>Enter your payment information</h2>
      <br/>
      <form action="" method="POST" id="payment-form">
        <p class="form-row">
        <label>Card Number</label>
        <input type="text" size="20" autocomplete="off" class="card-number" value="4242424242424242"/>
        </p>
        <p class="form-row">
        <label>CVC</label>
        <input type="text" size="4" autocomplete="off" class="card-cvc" value="123"/>
        </p>
        <p class="form-row">
        <label>Expiration (MM/YYYY)</label>
        <input type="text" size="2" class="card-expiry-month" value="12"/>
        <span> / </span>
        <input type="text" size="4" class="card-expiry-year" value="2013"/>
        </p>
        <button class="btn right submit-button" type="submit">Checkout</button>
      </form>
    {% endblock %}

Note that we include _stripe_head.html, that's the heavy lifting template that just pulls in the Stripe jscript.

Conclusion
-----------

That's really it for now. The bulk of our logic is the offsite_stripe.py file. 

TODOs
------

1. Allow user-configurable fields to validate. django-shop-stripe currently doesn't even check the billing address of a user (which is becoming increasingly passe with credit cards anyhow...)
2. Provide better, functional forms for the library. Do you know how to render id-less form field inputs with Django forms? Stripe requires that you have no IDs on inputs, which means the form data NEVER hits your server and you stay clean with the law.

