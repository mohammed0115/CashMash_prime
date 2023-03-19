from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
# from apps.distributors.models import Merchant, ServiceCenter
from .validators import CardHolderMobileNumberValidator
from datetime import datetime,date
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""


    """  welcome"""

    use_in_migrations = True

    def _create_user(self, card_holder_mobile_number, password, **extra_fields):
        """Create and save a User with the given card_holder_mobile_number and password."""
        if not card_holder_mobile_number:
            raise ValueError('The given card_holder_mobile_number must be set')
        card_holder_mobile_number = self.normalize_email(card_holder_mobile_number)
        user = self.model(card_holder_mobile_number=card_holder_mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, card_holder_mobile_number, password=None, **extra_fields):
        """Create and save a regular User with the given card_holder_mobile_number and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(card_holder_mobile_number, password, **extra_fields)

    def create_superuser(self, card_holder_mobile_number, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(card_holder_mobile_number, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    USER_TYPE_ADMIN = 0
    USER_TYPE_CARD_HOLDER = 1
    USER_TYPE_CHOICES = (
        (USER_TYPE_ADMIN, 'Admin'),
        (USER_TYPE_CARD_HOLDER, 'Card Holder'),
    )
    GENDER_CHOICES = (
        (0, 'Female'),
        (1, 'Male'),
    )

    username = models.CharField(_('full name'), max_length=100, blank=True, null=True)
    # email = models.EmailField(_('email address'), unique=True, db_index=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=False, db_index=True, blank=True, null=True)
    
    user_type = models.IntegerField(default=USER_TYPE_CARD_HOLDER, choices=USER_TYPE_CHOICES)
    date_of_birth = models.CharField(max_length=3,blank=True, null=True)
    # mobile_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    otp = models.CharField(max_length=50, blank=True, null=True)

    # Used only for card holders
    card_holder_mobile_number = models.CharField(_('mobile number'), max_length=20, unique=True,
                                                 blank=False, null=False,
                                                 validators=[CardHolderMobileNumberValidator()])
    card_holder_full_name = models.CharField(_('full name'), max_length=100, blank=True, null=True)
    card_holder_address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    card_holder_state = models.CharField(_('state'), max_length=100, blank=True, null=True)
    card_holder_city = models.CharField(_('city'), max_length=100, blank=True, null=True)

    CARD_HOLDER_ID_TYPE_NATIONAL_ID = 0
    CARD_HOLDER_ID_TYPE_PASSPORT = 1
    CARD_HOLDER_ID_TYPE_NATIONAL_NUMBER = 2
    CARD_HOLDER_ID_TYPE_DRIVE_LICENSE = 3
    CARD_HOLDER_ID_TYPE_CHOICES = (
        (CARD_HOLDER_ID_TYPE_NATIONAL_ID, _('National ID')),
        (CARD_HOLDER_ID_TYPE_PASSPORT, _('Passport Number')),
        (CARD_HOLDER_ID_TYPE_DRIVE_LICENSE, _('Driving License')),
    )
    card_holder_id_type = models.IntegerField(_('entityID type'), choices=CARD_HOLDER_ID_TYPE_CHOICES, blank=True, null=True)
    card_holder_id_number = models.CharField(_('ID number'), max_length=50, blank=True, null=True)
    card_holder_created_by = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name=_('User created by'), blank=True, null=True)
    jwt_secret_key = models.CharField(max_length=50, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'card_holder_mobile_number'
    REQUIRED_FIELDS = []  # remove email

    def __str__(self):
        # Only id is always available. If you want to change this,
        # make sure you always return a string but not None or other type
        if self.user_type is User.USER_TYPE_CARD_HOLDER:
            return "%s / %s" % (self.get_full_name(), self.get_mobile_number())
        else:
            return self.email if self.email else ''

    def clean(self):
        if self.email:
            # email is username field. it can be null or blank and it's unique,
            # so we shouldn't normalize it when it's empty.
            # Please check source code of base classes to find more details
            super(User, self).clean()

    def get_full_name(self):
        if self.user_type is User.USER_TYPE_CARD_HOLDER:
            return self.card_holder_full_name
        else:
            return super(User, self).get_full_name()

    def get_mobile_number(self):
        if self.user_type is User.USER_TYPE_CARD_HOLDER:
            return self.card_holder_mobile_number
        else:
            return self.mobile_number

    def get_user_information(self):
        if self.card_holder_created_by:
            return "{}, User id: {}".format(self.card_holder_created_by.get_full_name(), self.card_holder_created_by.id)

    def get_admin_url(self):
        return urlresolvers.reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))