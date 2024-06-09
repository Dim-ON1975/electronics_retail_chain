from django.contrib.auth.tokens import default_token_generator
from djoser.email import PasswordResetEmail, ActivationEmail, ConfirmationEmail, PasswordChangedConfirmationEmail, \
    UsernameChangedConfirmationEmail, UsernameResetEmail

from djoser import utils
from djoser.conf import settings

from core.settings import DOMAIN_FRONTEND, SITE_NAME_FRONTEND


class UserPasswordResetEmail(PasswordResetEmail):
    template_name = "djoser/email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail можно удалить
        context = super().get_context_data()

        user = context.get("user")
        context["domain"] = DOMAIN_FRONTEND
        context["site_name"] = SITE_NAME_FRONTEND
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class UserActivationEmail(ActivationEmail):
    template_name = "djoser/email/activation.html"

    def get_context_data(self):
        # ActivationEmail можно удалить
        context = super().get_context_data()

        user = context.get("user")
        context["domain"] = DOMAIN_FRONTEND
        context["site_name"] = SITE_NAME_FRONTEND
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


class UserConfirmationEmail(ConfirmationEmail):
    template_name = "djoser/email/confirmation.html"


class UserPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "djoser/email/password_changed_confirmation.html"


class UserUsernameChangedConfirmationEmail(UsernameChangedConfirmationEmail):
    template_name = "djoser/email/username_changed_confirmation.html"


class UserUsernameResetEmail(UsernameResetEmail):
    template_name = "djoser/email/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["domain"] = DOMAIN_FRONTEND
        context["site_name"] = SITE_NAME_FRONTEND
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
        return context
