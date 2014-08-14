from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User

from social.apps.django_app.default.models import Code


def password_reset_form(request):
    if request.method == 'POST':
        code = Code.make_code(request.POST['email'])
        send_reset_email(request, code)
        return render(request, 'password_reset_notification.html',
                      {'email': code.email})
    else:
        return render(request, 'password_reset_form.html')


def password_reset(request, code):
    code = Code.get_code(code)
    if code is None:
        raise Http404('Missing token')

    errors = []
    if request.method == 'POST':
        password = request.POST.get('password')
        password_verification = request.POST.get('password_verification')
        if password == password_verification:
            user = User.objects.get(email=code.email)
            user.set_password(password)
            user.save()
            code.verify()
            return redirect('login_form')
        else:
            errors.append('Passwords don\'t match')
    return render(request, 'password_reset.html', {'errors': errors})


def send_reset_email(request, code):
    url = reverse('password_reset', args=(code.code,))
    url = request.build_absolute_uri(url)
    send_mail('Password Recovery',
              'Use this URL to reset your password {0}'.format(url),
              settings.EMAIL_FROM, [code.email], fail_silently=False)
