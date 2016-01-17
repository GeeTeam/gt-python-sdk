# coding:utf-8
from flask import session, make_response, Flask, request, render_template
from geetest import GeetestLib
captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

@app.route('/getcaptcha', methods=["GET"])
def get_captcha():
    gt =  GeetestLib(captcha_id, private_key)
    status, response_str = gt.pre_process()
    session[gt.GT_STATUS_SESSION_KEY] = status
    return response_str

@app.route('/validate', methods=["POST"])
def validate_capthca():
    gt = GeetestLib(captcha_id, private_key)
    status = session[gt.GT_STATUS_SESSION_KEY]
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    gt = GeetestLib(captcha_id, private_key)
    result = gt.validate(status, challenge, validate, seccode)
    return result

@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run()