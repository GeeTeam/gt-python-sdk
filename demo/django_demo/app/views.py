# coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from geetest import GeetestLib

BASE_URL = "api.geetest.com/get.php?gt="
captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

def home(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def getcaptcha(request):
    gt = GeetestLib(captcha_id, private_key)
    status, response_str = gt.pre_process()
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    return HttpResponse(response_str)

def validate(request):
    if request.method == "POST":
        gt = GeetestLib(captcha_id, private_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        result = gt.validate(status, challenge, validate, seccode)
        return HttpResponse(result)
    return HttpResponse("error")
