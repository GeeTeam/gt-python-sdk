# coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
import sdk.geetest as geetest

BASE_URL = "api.geetest.com/get.php?gt="
captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

def home(request):
    gt = geetest.GeetestLib(captcha_id, private_key)
    url = ""
    httpsurl = ""
    try:
        challenge = gt.register_challenge()
    except:
        challenge = ""
    if len(challenge) == 32:
        url = "http://%s%s&challenge=%s&product=%s" % (BASE_URL, captcha_id, challenge, product)
    return render_to_response("index.html", {"url": url}, context_instance=RequestContext(request))

def login(request):
    gt = geetest.GeetestLib(captcha_id, private_key)
    if gt.pre_process():
        res_str = gt.success_pre_process()
        gt.set_gtserver_session(request.session.__setitem__, 1, gt.challenge)  #request.session['status'] = 1
    else:
        res_str = gt.fail_pre_process()
        gt.set_gtserver_session(request.session.__setitem__, 0, gt.challenge )  #request.session['status'] = 0
    return HttpResponse(res_str)

def validate(request):
    if request.method == "POST":
        challenge = request.POST.get('geetest_challenge', '')
        validate = request.POST.get('geetest_validate', '')
        seccode = request.POST.get('geetest_seccode', '')
        gt = geetest.GeetestLib(captcha_id, private_key)
        gt_challenge = gt.get_gtserver_challenge(request.session.__getitem__)
        gt_server_status = gt.get_gtserver_session(request.session.__getitem__)
        if not gt_challenge == challenge[0:32]:
            return HttpResponse("fail")
        if gt_server_status == 1:
            result = gt.post_validate(challenge, validate, seccode)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        return HttpResponse(result)
    return HttpResponse("error")
