Django Shop Stripe plugin  DEPRECATED
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

Here's an example to handle Stripe test input with a Stripe.js overlay. See the Stripe documentation for details, as well as other methods of integration.

    {% extends "base.html" %}

    {% block extra_head %}
    {% include "_stripe_head.html" %}
    {% endblock %}

    {% block content %}
    <form action="" method="POST">
    {% csrf_token %}
    <script
    src="https://checkout.stripe.com/checkout.js" class="stripe-button"
    data-key="YOUR_TEST_PUBLIC_KEY"
    data-amount="2000"
    data-name="Demo Site"
    data-description="2 widgets ($20.00)"
    data-image="/128x128.png">
    </script>
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
3. Tests.
