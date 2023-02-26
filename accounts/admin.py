from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import Http404, HttpResponseRedirect
from .models import User
from django.urls import reverse_lazy
# from .forms import AdminUserChangeForm, AdminUserCreationForm, ServiceCenterUserChangeForm, ServiceCenterUserCreationForm, MerchantUserChangeForm, MerchantUserCreationForm, CardHolderUserChangeForm, CardHolderUserCreationForm
from .forms import AdminUserChangeForm, AdminUserCreationForm, CardHolderUserChangeForm, CardHolderUserCreationForm

from django.contrib.auth.models import Group
from django.db import router, transaction
from Consumer.models import Card

class CardInline(admin.TabularInline):
    # template = 'accounts/headless_tabular_inline.html'
    model = Card
    fields = ('pan',)
    readonly_fields = ('pan',)
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""
    readonly_fields = ['last_login', 'date_joined', 'groups', 'readonly_full_name', 'readonly_mobile_number', 'readonly_card_holder_created_by']
    inlines = [CardInline, ]

    fieldsets_admin_user = (
        ('Personal info', {'fields': ('user_type', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # fieldsets_merchant_user = (
    #     (None, {'fields': ('user_type', 'merchant', 'first_name', 'last_name', 'date_of_birth', 'gender', 'mobile_number')}),
    #     ('Permissions', {'fields': ('is_active', 'groups')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )

    # fieldsets_service_center_user = (
    #     (None, {'fields': ('user_type', 'service_center', 'first_name', 'last_name', 'date_of_birth', 'gender', 'mobile_number')}),
    #     ('Permissions', {'fields': ('is_active', 'groups')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )

    fieldsets_card_holder_user = (
        (None, {'fields': ('user_type', 'card_holder_full_name', 'card_holder_mobile_number', 'email', 'date_of_birth', 'gender', 'card_holder_id_type', 'card_holder_id_number')}),
        ('Address', {'fields': ('card_holder_address', 'card_holder_city', 'card_holder_state')}),
        ('Distributor (either a merchant or a service center)', {'fields': ('merchant', 'service_center', 'readonly_card_holder_created_by')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets_admin_user = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type', 'email', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active',)})
    )

  

    # add_fieldsets_service_center_user = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('user_type', 'email', 'password1', 'password2'),
    #     }),
    #     ('Personal info', {'fields': ('service_center', 'first_name', 'last_name', 'date_of_birth', 'gender', 'mobile_number')}),
    #     ('Permissions', {'fields': ('is_active',)})
    # )

    add_fieldsets_card_holder_user = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type', 'card_holder_full_name', 'card_holder_mobile_number', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('email', 'date_of_birth', 'gender', 'card_holder_id_type', 'card_holder_id_number')}),
        ('Address', {'fields': ('card_holder_address', 'card_holder_city', 'card_holder_state')}),
        ('Distributor (either a merchant or a service center)', {'fields': ('merchant', 'service_center')}),
        ('Permissions', {'fields': ('is_active',)})
    )

    list_display = ('id', 'email', 'readonly_full_name', 'readonly_mobile_number', 'user_type', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)

    def readonly_mobile_number(self, obj):  # readonly
        return obj.get_mobile_number()

    readonly_mobile_number.short_description = 'mobile number'

    def readonly_full_name(self, obj):  # readonly
        return obj.get_full_name()
    readonly_full_name.short_description = 'full name'

    def readonly_card_holder_created_by(self, obj):
        return obj.get_user_information()

    readonly_card_holder_created_by.short_description = 'Card Holder created by'

    # def get_fieldsets(self, request, obj=None):
    #     if obj:
    #         if obj.user_type is User.USER_TYPE_ADMIN:
    #             return self.fieldsets_admin_user
    #         if obj.user_type is User.USER_TYPE_CARD_HOLDER:
    #             return self.fieldsets_card_holder_user
    #     else:
    #         user_type = int(request.GET.get("user_type", None))
    #         if user_type is User.USER_TYPE_ADMIN:
    #             return self.add_fieldsets_admin_user
    #         if user_type is User.USER_TYPE_CARD_HOLDER:
    #             return self.add_fieldsets_card_holder_user

    # def get_actions(self, request):
    #     actions = super(CustomUserAdmin, self).get_actions(request)
    #     if 'delete_selected' in actions and not self.has_delete_permission(request):
    #         del actions['delete_selected']
    #     return actions

    # def add_view(self, request, form_url='', extra_context=None):
    #     """
    #     This function is called when user click on add button. We check if this view has User Type passed in, if not, we
    #     redirect them to User Type selection page.
    #     """
    #     extra_context = extra_context or {}
    #     user_type = request.GET.get('user_type', None)
    #     if not user_type or int(user_type) not in dict(User.USER_TYPE_CHOICES):
    #         return HttpResponseRedirect(reverse_lazy("/"))
    #     else:
    #         user_type = int(user_type)
    #         if user_type is User.USER_TYPE_ADMIN:
    #             extra_context['title'] = 'Add admin user'
    #         if user_type is User.USER_TYPE_CARD_HOLDER:
    #             extra_context['title'] = 'Add card holder user'
    #         with transaction.atomic(using=router.db_for_write(self.model)):
    #             return self._add_view(request, form_url, extra_context)

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Use special form during user creation to show the relevant fields for different type of users.
    #     """
    #     if obj:
    #         user_type = obj.user_type
    #         if user_type is User.USER_TYPE_ADMIN:
    #             self.form = AdminUserChangeForm
          
    #         if user_type is User.USER_TYPE_CARD_HOLDER:
    #             self.form = CardHolderUserChangeForm
    #     else:
    #         user_type = int(request.GET.get("user_type", None))
    #         if user_type is User.USER_TYPE_ADMIN:
    #             self.add_form = AdminUserCreationForm
    #         if user_type is User.USER_TYPE_CARD_HOLDER:
    #             self.add_form = CardHolderUserCreationForm

    #     return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     """
    #     Given a model instance save it to the database.
    #     We manually apply the user type and user group to the user when adding a new one.
    #     """
    #     if not change:  # adding a user
    #         if obj.user_type is User.USER_TYPE_ADMIN:
    #             obj.is_staff = True
    #         else:
    #             obj.is_staff = False
    #     obj.save()
    #     if not change:  # update group
    #         if obj.user_type is User.USER_TYPE_ADMIN:
    #             (g, created) = Group.objects.get_or_create(name='Administrator')
    #             obj.groups.add(g)
        
    #         if obj.user_type is User.USER_TYPE_CARD_HOLDER:
    #             (g, created) = Group.objects.get_or_create(name='Card Holder')
    #             obj.groups.add(g)
    #     obj.save()

    # def response_add(self, request, obj, post_url_continue=None):
    #     if post_url_continue is None:
    #         post_url_continue = reverse_lazy('admin:accounts_user_changelist')
    #     return super(UserAdmin, self).response_add(request, obj, post_url_continue)

admin.site.register(User, CustomUserAdmin)
