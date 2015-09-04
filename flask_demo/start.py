# coding:utf-8
import sdk.geetest as geetest
from flask import Flask, render_template, request

BASE_URL = "api.geetest.com/get.php?gt="

captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SERVER_NAME='127.0.0.1:5000'
)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        challenge = request.form['geetest_challenge']
        validate = request.form['geetest_validate']
        seccode = request.form['geetest_seccode']
        gt = geetest.geetest(captcha_id, private_key)
        result = gt.geetest_validate(challenge, validate, seccode)
        if result:
            return "success"
        else:
            return "fail"
    else:
        gt = geetest.geetest(captcha_id, private_key)
        url = ""
        httpsurl = ""
        try:
            challenge = gt.geetest_register()
        except Exception as e:
            challenge = ""
        if len(challenge) == 32:
            url = "http://%s%s&challenge=%s&product=%s" % (BASE_URL, captcha_id, challenge, product)
            httpsurl = "https://%s%s&challenge=%s&product=%s" % (BASE_URL, captcha_id, challenge, product)
        return render_template('login.html', url=url, httpsurl=httpsurl)


if __name__ == '__main__':
    app.run()