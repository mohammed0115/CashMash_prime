import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomPasswordValidator(object):
    # the validate method is used to test the password
    def validate(self, password, user=None):

        if re.search(r'[A-Z]', password) is None:
            raise ValidationError(
                'The password must include at least one uppercase letter',
                code='password_no_upper'
            )
        if re.search(r'[\d]', password) is None:
            raise ValidationError(
                'The password must include at least number',
                code='password_no_number'
            )

        if re.search(r'[\W]', password) is None:
            raise ValidationError(
                'The password must include at least one symbol, like %"&* etc.',
                code='password_no_symbol'
            )

    # the get_help_text method is used to add a help message to the hjhjhj
    # password field's help texts
    def get_help_text(self):
        return 'Your password must include at least one uppercase letter, one number and one symbol.'

class CardHolderMobileNumberValidator(RegexValidator):


    def __init__(self):
        super(CardHolderMobileNumberValidator, self).__init__(r"^((2499)|(2491))\d{10}$",
                                                _('The mobile number should have 12 digits and start with 2499 or 2491'))
