from django.conf.urls import  url

urlpatterns = ['',
    url(r'^pc-geetest/register', 'app.views.pcgetcaptcha', name='pcgetcaptcha'),
    url(r'^mobile-geetest/register', 'app.views.mobilegetcaptcha', name='mobilegetcaptcha'),
    url(r'^pc-geetest/validate$', 'app.views.pcvalidate', name='pcvalidate'),
    url(r'^pc-geetest/ajax_validate','app.views.pcajax_validate', name='pcajax_validate'),
    url(r'^mobile-geetest/ajax_validate','app.views.mobileajax_validate', name='mobileajax_validate'),
    url(r'/*', 'app.views.home', name='home'),
]
