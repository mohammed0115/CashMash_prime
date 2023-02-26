from accounts.models import User
from Consumer.auth.authentication import AccessTokenAuthentication

from APIKEY.models import BlockedToken


def authenticate_card_holder_user(mobile_number=None, password=None):
    """
    This is the function to authenticate a cardholder user by validating mobile_number and password.
    Extend this to support more complicated authentication logic
    :return: the user instance identified by the credentials
    """
    UserModel = User

    try:
        user = UserModel._default_manager.get(card_holder_mobile_number=mobile_number)
        if user.user_type is User.USER_TYPE_CARD_HOLDER:
            if user.check_password(password):
                return user
        else:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    except UserModel.DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a non-existing user (#20760).
        UserModel().set_password(password)


class CardHolderAccessTokenAuthentication(AccessTokenAuthentication):

    def get_user_by_username(self, username):
        return User.objects.get(card_holder_mobile_number=username)

    def is_blacklisted(self, token):
        return BlockedToken.objects.filter(token=token).exists()