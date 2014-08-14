from django.contrib.auth.models import User

from social.exceptions import AuthFailed
from social.pipeline.mail import mail_validation as psa_mail_validation


def user_by_email(backend, details, *args, **kwargs):
    if backend.name == 'email':
        if not details.get('email'):
            raise AuthFailed(backend, 'Missing email')

        request_data = backend.strategy.request_data()
        password = request_data.get('password')
        if not request_data.get('verification_code') and not password:
            raise AuthFailed(backend, 'Missing password')

        try:
            user = User.objects.get(email=details['email'])
        except User.DoesNotExist:
            user = None
        else:
            if not request_data.get('verification_code') and \
               not user.check_password(password):
                raise AuthFailed(backend, 'Wrong password')
        return {'user': user, 'password': password}


def set_password(backend, user, is_new=False, *args, **kwargs):
    if backend.name == 'email' and is_new:
        user.set_password(kwargs['password'])
        user.save()


def mail_validation(*args, **kwargs):
    if kwargs.get('user') is None:
        return psa_mail_validation(*args, **kwargs)
