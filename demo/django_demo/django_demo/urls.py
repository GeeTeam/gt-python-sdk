from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register', 'app.views.getcaptcha', name='getcaptcha'),
    url(r'^validate$', 'app.views.validate', name='validate'),
    url(r'^ajax_validate','app.views.ajax_validate', name='ajax_validate'),
    url(r'/*', 'app.views.home', name='home'),
)
