from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login$', 'app.views.login', name='login'),
    url(r'/*', 'app.views.home', name='home'),

)
