from setuptools import setup, find_packages

setup(
    name='django-shop-stripe',
    version=__import__('shop_stripe').__version__,
    license="BSD",

    install_requires = [],

    description='Let us use stripe for payments with django-shop.',
    long_description=open('README').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-shop-stripe',
    download_url='http://github.com/powellc/django-shop-stripe/downloads',

    include_package_data=True,

    packages=['shop_stripe'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
