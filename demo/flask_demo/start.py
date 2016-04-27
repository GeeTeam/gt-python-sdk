# coding:utf-8
import json

from flask import session, make_response, Flask, request, render_template
from geetest import GeetestLib

captcha_id = "b46d1900d0a894591916ea94ea91bd2c"
private_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


@app.route('/register', methods=["GET"])
def get_captcha():
    user_id = 'test'
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str


@app.route('/validate', methods=["POST"])
def validate_capthca():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
        print 111
    else:
        result = gt.failback_validate(challenge, validate, seccode)
        print 222
    result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
    return result

@app.route('/ajax_validate', methods=["POST"])
def ajax_validate():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
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