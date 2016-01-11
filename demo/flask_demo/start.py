# coding:utf-8
from flask import session, make_response, Flask, request, render_template
from sdk.geetestlib import GeetestLib

id = "a40fd3b0d712165c5d13e6f747e948d4"
key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    #SERVER_NAME='127.0.0.1:5000'
)

@app.route('/getcaptcha', methods=["GET"])
def get_captcha():
    gt =  GeetestLib(id, key)
    if gt.pre_process():
        res_str = gt.success_pre_process()
        gt.set_gtserver_session(session.__setitem__, 1, gt.challenge)
    else:
        res_str = gt.fail_pre_process()
        gt.set_gtserver_session(session.__setitem__, 0, gt.challenge)
    return res_str

@app.route('/validate', methods=["POST"])
def validate_capthca():
    challenge = request.form['geetest_challenge']
    validate = request.form['geetest_validate']
    seccode = request.form['geetest_seccode']
    gt = GeetestLib(id,key)
    gt.challenge = gt.get_gtserver_challenge(session.__getitem__)
    gt_server_status = gt.get_gtserver_session(session.__getitem__)
    if gt_server_status == 1:
        result = gt.post_validate(challenge, validate, seccode)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    return result

@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run()