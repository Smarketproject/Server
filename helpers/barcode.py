from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

error_messages = {
    'digits_only': _("This field requires only numbers."),
    'max_digits': _("This field requires exactly 13 digits.")
}

def validate_ean(value):
    if value in EMPTY_VALUES:
        return u''
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages['digits_only'])
    if len(value) != 13:
        raise ValidationError(error_messages['max_digits'])
"""
def computeChecksum(self, value):


    weight=[1,3]*6
    magic=10
    sum = 0
           
    for i in range(12):         
        sum = sum + int(value[i]) * weight[i]
    z = ( magic - (sum % magic) ) % magic
    if z < 0 or z >= magic:
        return None
    return z
 """
     