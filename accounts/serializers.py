from django.utils.translation import ugettext as _
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group
from django.db import transaction

from rest_framework import serializers
from rest_framework import validators
from Consumer.auth.serializers import BaseObtainTokenSerializer
from accounts.models import User
from accounts.validators import CardHolderMobileNumberValidator, CustomPasswordValidator
from Consumer.auth.authentication import validate_password
from Consumer.authentication import authenticate_card_holder_user


class CardHolderUserLoginRequestSerializer(BaseObtainTokenSerializer):
    user_model_username_field = 'card_holder_mobile_number'

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(BaseObtainTokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(validators=[CardHolderMobileNumberValidator()])

    @property
    def username_field(self):  # this field is only used by serializer as field name but not by user model
        return "mobile_number"

    def authenticate(self, username, password):
        return authenticate_card_holder_user(username, password)


class CardHolderUserRetrieveSerializer(serializers.ModelSerializer):
    """
    The serializer used when retrieving user details
    """
    mobile_number = serializers.CharField(source='card_holder_mobile_number',
                                          validators=[CardHolderMobileNumberValidator(),
                                                      validators.UniqueValidator(queryset=User.objects.all())])
    full_name = serializers.CharField(source='card_holder_full_name')
    address = serializers.CharField(source='card_holder_address',allow_null=True, required=False,allow_blank=True)
    state = serializers.CharField(source='card_holder_state',allow_null=True, required=False,allow_blank=True)
    city = serializers.CharField(source='card_holder_city',allow_null=True, required=False,allow_blank=True)
    id_type = serializers.ChoiceField(source='card_holder_id_type', choices=User.CARD_HOLDER_ID_TYPE_CHOICES, allow_null=True, required=False,allow_blank=True)
    id_number = serializers.CharField(source='card_holder_id_number',allow_null=True, required=False,allow_blank=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'mobile_number', 'email', 'gender', 'date_of_birth',
                  'address', 'state', 'city', 'id_type', 'id_number')





class CardHolderUserCreationSerializer1(CardHolderUserRetrieveSerializer,BaseObtainTokenSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(BaseObtainTokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(validators=[CardHolderMobileNumberValidator()])

    
    @property
    def username_field(self):  # this field is only used by serializer as field name but not by user model
        return "mobile_number"
    def authenticate(self, username, password):
        return authenticate_card_holder_user(username, password)
    class Meta:
        model = User
        fields = ('id', 'full_name', 'mobile_number', 'email', 'gender',
                  'date_of_birth', 'address', 'state', 'city', 'id_type', 'id_number',
                  'password', 'password2')
    
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': _("The two password fields didn't match.")}, code='passwords_not_match')
        else:
            return data
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        mobile_number=validated_data.pop('mobile_number')
        validated_data['card_holder_mobile_number']=mobile_number
        with transaction.atomic():
            card_holder = User(**validated_data)
            card_holder.user_type = User.USER_TYPE_CARD_HOLDER
            card_holder.set_password(password)
            card_holder.is_active = True
            card_holder.save()
            (g, created) = Group.objects.get_or_create(name='Card Holder')
            card_holder.groups.add(g)
            card_holder.save()
            return card_holder
    
class CardHolderUserCreationSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(source='card_holder_mobile_number',
                                          validators=[CardHolderMobileNumberValidator(),
                                                      validators.UniqueValidator(queryset=User.objects.all())])
    full_name = serializers.CharField(source='card_holder_full_name', max_length=100)
    address = serializers.CharField(source='card_holder_address', max_length=255, allow_null=True, required=False)
    state = serializers.CharField(source='card_holder_state', max_length=100, allow_null=True, required=False)
    city = serializers.CharField(source='card_holder_city', max_length=100, allow_null=True, required=False)
    id_type = serializers.ChoiceField(source='card_holder_id_type', choices=User.CARD_HOLDER_ID_TYPE_CHOICES, allow_null=True, allow_blank=True, required=False)
    id_number = serializers.CharField(source='card_holder_id_number', max_length=50, allow_null=True, allow_blank=True, required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'mobile_number', 'email', 'gender',
                  'date_of_birth', 'address', 'state', 'city', 'id_type', 'id_number',
                  'password1', 'password2')

    def validate_password1(self, password):
        password_validators = [
            CustomPasswordValidator(),
            password_validation.MinimumLengthValidator(min_length=8),
            password_validation.CommonPasswordValidator(),
            password_validation.NumericPasswordValidator()
        ]
        validate_password(password, None, password_validators=password_validators)
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': _("The two password fields didn't match.")}, code='passwords_not_match')
        has_id_type = 'card_holder_id_type' in data
        has_id_number = 'card_holder_id_number' in data

        id_type = data.get('card_holder_id_type', None)
        id_number = data.get('card_holder_id_number', None)

        if has_id_type and not has_id_number:
            raise serializers.ValidationError({'id_number': _("ID number is required when id type is provided.")}, code='required')
        if has_id_number and not has_id_type:
            raise serializers.ValidationError({'id_type': _("ID type is required when id number is provided.")}, code='required')
        if has_id_type and has_id_number:
            if not id_type:
                raise serializers.ValidationError({'id_type': _("ID type may not be null or blank when id number is provided.")}, code='blank')
            if not id_number:
                raise serializers.ValidationError({'id_number': _("ID number may not be null or blank when id type is provided.")}, code='blank')

        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        with transaction.atomic():
            card_holder = User(**validated_data)
            card_holder.user_type = User.USER_TYPE_CARD_HOLDER
            card_holder.set_password(password)
            card_holder.is_active = True
            card_holder.save()
            (g, created) = Group.objects.get_or_create(name='Card Holder')
            card_holder.groups.add(g)
            card_holder.save()
            return card_holder

    def update(self, instance, validated_data):
        raise Exception('CardHolderUserCreationSerializer should be used only '
                        'when create a user. Update is not supported')
