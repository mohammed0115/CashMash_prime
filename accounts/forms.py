from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User
from django.forms.widgets import SelectDateWidget
import datetime
from django.utils.translation import ugettext, ugettext_lazy as _

# the default datepicker is difficult to use for birthdays so using a different widget
# so that year, month and date can be picked separately
birthday_widget = SelectDateWidget(
    years=range(datetime.datetime.now().year,1920,-1),
    empty_label=("Year", "Month", "Day"),)


##### USER FORMS ######

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserTypeSelectionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_type']


##### MERCHANT USER FORMS ######

# class MerchantUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(MerchantUserCreationForm, self).__init__(*args, **kwargs)

#         self.fields['email'].required = True
#         self.fields['date_of_birth'].required = True
#         self.fields['date_of_birth'].widget = birthday_widget
#         self.fields['mobile_number'].required = True
#         self.fields['gender'].required = True
#         self.fields['merchant'].required = True

#         self.fields['user_type'].required = True
#         self.fields['user_type'].initial = User.USER_TYPE_MERCHANT
#         self.fields['user_type'].widget = forms.HiddenInput()


# class MerchantUserChangeForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(MerchantUserChangeForm, self).__init__(*args, **kwargs)
#         self.fields['date_of_birth'].required = True
#         self.fields['date_of_birth'].widget = birthday_widget
#         self.fields['mobile_number'].required = True
#         self.fields['gender'].required = True
#         self.fields['merchant'].required = True
#         self.fields['user_type'].disabled = True


##### ADMIN USER FORMS ######

class AdminUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['user_type'].required = True
        self.fields['user_type'].initial = User.USER_TYPE_ADMIN
        self.fields['user_type'].widget = forms.HiddenInput()


class AdminUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(AdminUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].disabled = True


##### SERVICE CENTER USER FORMS ######

# class ServiceCenterUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(ServiceCenterUserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['email'].required = True
#         self.fields['date_of_birth'].required = True
#         self.fields['date_of_birth'].widget = birthday_widget
#         self.fields['mobile_number'].required = True
#         self.fields['gender'].required = True
#         self.fields['service_center'].required = True

#         self.fields['user_type'].required = True
#         self.fields['user_type'].initial = User.USER_TYPE_SERVICE_CENTER
#         self.fields['user_type'].widget = forms.HiddenInput()


# class ServiceCenterUserChangeForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(ServiceCenterUserChangeForm, self).__init__(*args, **kwargs)
#         self.fields['date_of_birth'].required = True
#         self.fields['date_of_birth'].widget = birthday_widget
#         self.fields['mobile_number'].required = True
#         self.fields['gender'].required = True
#         self.fields['service_center'].required = True
#         self.fields['user_type'].disabled = True



##### CARD HOLDER USER FORMS ######

class CardHolderUserCreationForm(BaseUserCreationForm):
    BaseUserCreationForm.error_messages.update({
        'distributor_conflict': _("You can either select a merchant or a service center but not both"),
    })

    def __init__(self, *args, **kwargs):
        super(CardHolderUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = birthday_widget
        self.fields['card_holder_mobile_number'].required = True
        self.fields['card_holder_full_name'].required = True

        self.fields['user_type'].required = True
        self.fields['user_type'].initial = User.USER_TYPE_CARD_HOLDER
        self.fields['user_type'].widget = forms.HiddenInput()

    def clean_service_center(self):
        sc = self.cleaned_data.get("service_center")
        merchant = self.cleaned_data.get("merchant")
        if sc and merchant:
            raise forms.ValidationError(
                self.error_messages['distributor_conflict'],
                code='distributor_conflict',
            )
        return sc


class CardHolderUserChangeForm(forms.ModelForm):
    error_messages = {
        'distributor_conflict': _("You can either select a merchant or a service center but not both"),
    }

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CardHolderUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = birthday_widget
        self.fields['card_holder_mobile_number'].required = True
        self.fields['user_type'].disabled = True
        self.fields['card_holder_full_name'].required = True

    # def clean_service_center(self):
    #     sc = self.cleaned_data.get("service_center")
    #     merchant = self.cleaned_data.get("merchant")
    #     if sc and merchant:
    #         raise forms.ValidationError(
    #             self.error_messages['distributor_conflict'],
    #             code='distributor_conflict',
            # )
        return sc