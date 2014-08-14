from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^password-reset/$', 'recovery.views.password_reset_form',
        name='password_reset_form'),
    url(r'^password-reset/(?P<code>[^/]+)/$', 'recovery.views.password_reset',
        name='password_reset'),
)
