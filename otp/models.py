from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import CardHolderMobileNumberValidator


class OTP(models.Model):

    card_holder_mobile_number = models.CharField(
        _("mobile number"),
        max_length=20,
        validators=[CardHolderMobileNumberValidator()], default=None
    )
    private_key = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
