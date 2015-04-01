from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
import sdk.geetest as geetest

BASE_URL = "api.geetest.com/get.php?gt="

captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"


def home(request):
    gt = geetest.geetest(captcha_id, private_key)
    url = ""
    httpsurl = ""
    try:
        challenge = gt.geetest_register()
    except:
        challenge = ""
    if len(challenge) == 32:
        url = "http://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
        httpsurl = "https://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
    return render_to_response("index.html", {"url": url}, context_instance=RequestContext(request))


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