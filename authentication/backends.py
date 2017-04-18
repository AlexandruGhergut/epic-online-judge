from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = super(EmailOrUsernameBackend, self).authenticate(username,
                                                                password,
                                                                **kwargs)

        if user is not None:
            return user

        if '@' in username:
            email = username
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password) and \
                        self.user_can_authenticate(user):
                            return user
