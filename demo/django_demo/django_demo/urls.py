from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^getcaptcha$', 'app.views.getcaptcha', name='getcaptcha'),
    url(r'^validate$', 'app.views.validate', name='validate'),
    url(r'/*', 'app.views.home', name='home'),
)
