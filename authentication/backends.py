from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from oauth2client import client, crypt

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = super(EmailOrUsernameBackend, self).authenticate(username,
                                                                password,
                                                                **kwargs)

        if user is not None:
            return user

        if username and '@' in username:
            email = username
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password) and \
                        self.user_can_authenticate(user):
                            return user

        return None


class GoogleSignInBackend(object):
    def authenticate(self, token=None):
        try:
            idinfo = client.verify_id_token(token, settings.GOOGLE_CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                    raise crypt.AppIdentityError("Wrong issuer.")
        except crypt.AppIdentityError:
            return None

        user = User.objects.filter(email=idinfo['email']).first()
        if not user:
            user = User.objects.create(username=idinfo['sub'],
                                       email=idinfo['email'])
            user.is_active = idinfo['email_verified']
            user.set_unusable_password()
            user.save()
            user.profile.first_name = idinfo['given_name']
            user.profile.last_name = idinfo['family_name']
            user.profile.email_confirmed = idinfo['email_verified']
            user.profile.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
