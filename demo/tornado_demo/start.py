# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.gen
from torndsession.sessionhandler import SessionBaseHandler
from geetest import GeetestLib

captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/login.html",)

class GetCaptchaHandler(SessionBaseHandler):
    def get(self):
        gt = GeetestLib(captcha_id, private_key)
        status, response_str = gt.pre_process()
        self.session[gt.GT_STATUS_SESSION_KEY] = status
        self.write(response_str)

class ValidateHandler(SessionBaseHandler):
    def post(self):
        gt = GeetestLib(captcha_id, private_key)
        challenge = self.get_argument(gt.FN_CHALLENGE, "")
        validate = self.get_argument(gt.FN_VALIDATE, "")
        seccode = self.get_argument(gt.FN_SECCODE, "")
        status = self.session[gt.GT_STATUS_SESSION_KEY]
        result = gt.validate(status, challenge, validate, seccode)
        self.write(result)

if __name__ == "__main__":
    app = tornado.web.Application([
                                      (r"/", MainHandler),
                                      (r"/getcaptcha", GetCaptchaHandler),
                                      (r"/validate", ValidateHandler)
                                  ], debug=True)

    app.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
