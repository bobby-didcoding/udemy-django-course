# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
from djoser import email


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'emails/users/password_reset_email.html'