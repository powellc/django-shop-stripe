# Taken and modified from django-stripe project
import types, datetime

from django import forms
from django.utils.translation import ugettext as _

FORM_PREIX = 'stripe'

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in xrange(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

def make_widget_anonymous(widget):
    def _anonymous_render(instance, name, value, attrs=None):
        return instance._orig_render('', value, attrs)

    widget._orig_render = widget.render
    widget.render = types.MethodType(_anonymous_render, widget)

    return widget

class CardForm(forms.Form):
    number = forms.CharField(label=_("Card number"))
    exp_month = forms.CharField(label=_("Expiration month"), widget=forms.Select(choices=MONTH_CHOICES))
    exp_year = forms.CharField(label=_("Expiration year"), widget=forms.Select(choices=YEAR_CHOICES))

    def get_cvc_field(self):
        return forms.CharField(label=_("Security code (CVV)"))

    def __init__(self, validate_cvc=True, prefix=FORM_PREIX, *args, **kwargs):
        super(CardForm, self).__init__(prefix=prefix, *args, **kwargs)

        if validate_cvc:
            self.fields['cvc'] = self.get_cvc_field()

class AnonymousCardForm(CardForm):
    def __init__(self, *args, **kwargs):
        super(AnonymousCardForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            make_widget_anonymous(self.fields[key].widget)
