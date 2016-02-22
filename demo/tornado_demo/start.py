# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.gen
from torndsession.sessionhandler import SessionBaseHandler
from geetest import GeetestLib

captcha_id = "b46d1900d0a894591916ea94ea91bd2c"
private_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/login.html",)

class GetCaptchaHandler(SessionBaseHandler):
    def get(self):
        gt = GeetestLib(captcha_id, private_key)
        status= gt.pre_process()
        self.session[gt.GT_STATUS_SESSION_KEY] = status
        response_str = gt.get_response_str()
        self.write(response_str)

class ValidateHandler(SessionBaseHandler):
    def post(self):
        print self.session
        gt = GeetestLib(captcha_id, private_key)
        challenge = self.get_argument(gt.FN_CHALLENGE, "")
        validate = self.get_argument(gt.FN_VALIDATE, "")
        seccode = self.get_argument(gt.FN_SECCODE, "")
        status = self.session[gt.GT_STATUS_SESSION_KEY]
        if status:
            result = gt.success_validate(challenge, validate, seccode)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = "sucess" if result else "fail"
        self.write(result)

if __name__ == "__main__":
    app = tornado.web.Application([
                                      (r"/", MainHandler),
                                      (r"/getcaptcha", GetCaptchaHandler),
                                      (r"/validate", ValidateHandler)
                                  ], debug=True)

    app.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
