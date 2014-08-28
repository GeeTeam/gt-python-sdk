#!coding:utf8
import geetest
import web
gt=geetest.geetest("0f1a37e33c9ed10dd2e133fe2ae9c459")
urls = ("/", "hello",
    "/log","log")
app = web.application(urls, globals())

class hello:
    def GET(self):
        f=open("login.html","r")
        return f.read()
class log:
    def GET(self):
        i = web.input()
        challenge=i.geetest_challenge
        validate=i.geetest_validate
        seccode=i.geetest_seccode
        print 'challenge'+challenge;print 'validate'+validate;print 'seccode'+seccode
        if gt.geetest_validate(challenge,validate,seccode):
            return "OK"
        else:
            return "false"


if __name__ == "__main__":
    app.run()


















"""
from gevent.pywsgi import WSGIServer
gt=geetest.geetest("9bf96071b80aa0a64b8041ccc703c0c2")
def start_server(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html;charset=UTF-8')
    ]
    start_response(status,headers)
    print environ
    if environ["PATH_INFO"]=="/":
        f=open("login.html","r")
        return f.read()
    else:
        if gt.geetest_validate(challenge,validate):
            return "OK"
        else:
            return "false"




def main():
    WSGIServer(('', 8000), start_server).serve_forever()


if __name__ == '__main__':
    main()
"""
