#coding:utf-8
import json

from flask import session, make_response, Flask, request, render_template
from geetest import GeetestLib

pc_geetest_id = "6f1ecf26ea05d03584319348bfc7594b"
pc_geetest_key = "05ff7b722d3ad37304db391e121da926"
mobile_geetest_id = "48a6ebac4ebc6642d68c217fca33eb4d"
mobile_geetest_key = "4f1c085290bec5afdc54df73535fc361"
app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


@app.route('/pc-geetest/register', methods=["GET"])
def get_pc_captcha():
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str

@app.route('/mobile-geetest/register', methods=["GET"])
def get_mobile_captcha():
    user_id = 'test'
    gt = GeetestLib(mobile_geetest_id, mobile_geetest_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str

@app.route('/pc-geetest/validate', methods=["POST"])
def pc_validate_captcha():
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
    return result

@app.route('/pc-geetest/ajax_validate', methods=["POST"])
def pc_ajax_validate():
    gt = GeetestLib(pc_geetest_id,pc_geetest_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id,data='',userinfo='')
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    result = {"status":"success"} if result else {"status":"fail"}
    return json.dumps(result)

@app.route('/mobile-geetest/ajax_validate', methods=["POST"])
def mobile_ajax_validate():
    gt = GeetestLib(mobile_geetest_id,mobile_geetest_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id,data='',userinfo='')
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    result = {"status":"success"} if result else {"status":"fail"}
    return json.dumps(result)

@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run()
