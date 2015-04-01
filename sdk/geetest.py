#!coding:utf8
from hashlib import md5
import urllib2


class geetest(object):
    """docstring for gt"""

    def __init__(self, id, key):
        self.PRIVATE_KEY = key
        self.CAPTCHA_ID = id
        self.PY_VERSION = "2.15.4.1.1"

    def geetest_register(self):
        apireg = "http://api.geetest.com/register.php?"
        regurl = apireg + "gt=%s"%self.CAPTCHA_ID
        try:
            result = urllib2.urlopen(regurl, timeout=2).read()
        except:
            result = ""
        return result

    def geetest_validate(self, challenge, validate, seccode):
        apiserver = "http://api.geetest.com/validate.php"
        if validate == self.md5value(self.PRIVATE_KEY + 'geetest' + challenge):
            query = 'seccode=' + seccode + "&sdk=python_" + self.PY_VERSION
            print query
            backinfo = self.postvalues(apiserver, query)
            if backinfo == self.md5value(seccode):
                return 1
            else:
                return 0
        else:
            return 0

    def postvalues(self, apiserver, data):
        req = urllib2.Request(apiserver)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        backinfo = response.read()
        return backinfo

    def md5value(self, values):
        m = md5()
        m.update(values)
        return m.hexdigest()
