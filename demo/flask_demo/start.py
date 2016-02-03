# coding:utf-8
from flask import session, make_response, Flask, request, render_template
from geetest import GeetestLib
captcha_id = "b46d1900d0a894591916ea94ea91bd2c"
private_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

@app.route('/getcaptcha', methods=["GET"])
def get_captcha():
    gt =  GeetestLib(captcha_id, private_key)
    status = gt.pre_process()
    session[gt.GT_STATUS_SESSION_KEY] = status
    response_str = gt.get_response_str()
    return response_str

@app.route('/validate', methods=["POST"])
def validate_capthca():
    gt = GeetestLib(captcha_id, private_key)
    status = session[gt.GT_STATUS_SESSION_KEY]
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    if status:
        result = gt.success_validate(challenge, validate, seccode)
    else:
        result = gt.fail_validate(challenge, validate, seccode)
    result = "sucess" if result else "fail"
    return result

@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run()