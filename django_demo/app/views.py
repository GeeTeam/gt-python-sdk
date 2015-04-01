from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
import sdk.geetest as geetest


captcha_id = "17e0a0be98b00ed5e5b263931f3156d9"
private_key = "*****"


def home(request):
    gt = geetest.geetest(captcha_id, private_key)
    try:
        challenge = gt.geetest_register()
    except:
        challenge = ""
    return render_to_response("index.html", {"challenge": challenge}, context_instance=RequestContext(request))


def login(request):
    if request.method == "POST":
        challenge = request.POST.get('geetest_challenge', '')
        validate = request.POST.get('geetest_validate', '')
        seccode = request.POST.get('geetest_seccode', '')
        # print challenge
        # print validate
        # print seccode
        gt = geetest.geetest(captcha_id, private_key)
        result = gt.geetest_validate(challenge, validate, seccode)
        if result:
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
    else:
        return HttpResponse("e")