# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.gen
from torndsession.sessionhandler import SessionBaseHandler
from geetest import GeetestLib

import json

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
        user_id = 'test'
        gt = GeetestLib(captcha_id, private_key)
        status = gt.pre_process(user_id)
        self.session[gt.GT_STATUS_SESSION_KEY] = status
        self.session["user_id"] = user_id
        response_str = gt.get_response_str()
        self.write(response_str)


class ValidateHandler(SessionBaseHandler):
    def post(self):
        gt = GeetestLib(captcha_id, private_key)
        challenge = self.get_argument(gt.FN_CHALLENGE, "")
        validate = self.get_argument(gt.FN_VALIDATE, "")
        seccode = self.get_argument(gt.FN_SECCODE, "")
        status = self.session[gt.GT_STATUS_SESSION_KEY]
        user_id = self.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
            self.session["user_id"] = user_id
        result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
        self.write(result)


class AjaxValidateHandler(SessionBaseHandler):
    def post(self):
        gt = GeetestLib(captcha_id, private_key)
        challenge = self.get_argument(gt.FN_CHALLENGE, "")
        validate = self.get_argument(gt.FN_VALIDATE, "")
        seccode = self.get_argument(gt.FN_SECCODE, "")
        status = self.session[gt.GT_STATUS_SESSION_KEY]
        user_id = self.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
            self.session["user_id"] = user_id
        result = result = {"status":"success"} if result else {"status":"fail"}
        self.write(json.dumps(result))

if __name__ == "__main__":
    app = tornado.web.Application([
                                      (r"/", MainHandler),
                                      (r"/register", GetCaptchaHandler),
                                      (r"/validate", ValidateHandler),
                                      (r"/ajax_validate", AjaxValidateHandler)
                                  ], debug=True)

    app.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
