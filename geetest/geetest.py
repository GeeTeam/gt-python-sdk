#!coding:utf8
import string
import urllib2
import random
import json
from hashlib import md5
from urllib import urlencode


VERSION = "3.0.0"


class GeetestLib(object):

    FN_CHALLENGE = "geetest_challenge"
    FN_VALIDATE = "geetest_validate"
    FN_SECCODE = "geetest_seccode"

    GT_STATUS_SESSION_KEY = "gt_server_status"

    SUCCESS_RES = "success"
    FAIL_RES = "fail"

    API_URL = "http://api.geetest.com"
    REGISTER_HANDLER = "/register.php"
    VALIDATE_HANDLER = "/validate.php"


    def __init__(self, captcha_id, private_key):
        self.private_key = private_key                    #私钥
        self.captcha_id = captcha_id                      #公钥
        self.sdk_version = VERSION              #SDK版本

    def pre_process(self):
        """
        验证初始化预处理.
        """
        status, challenge = self._register()
        return status, self._make_response_format(status, challenge)

    def _register(self):
        challenge = self._register_challenge()
        if len(challenge) == 32:
            return 1, challenge
        else:
            return 0, self._make_fail_challenge()

    def _make_fail_challenge(self):
        rnd1 = random.randint(0, 99)
        rnd2 = random.randint(0, 99)
        md5_str1 = self._md5_encode(str(rnd1))
        md5_str2 = self._md5_encode(str(rnd2))
        challenge = md5_str1 + md5_str2[0:2]
        return challenge

    def _make_response_format(self, success=1, challenge=None):
        if not challenge:
            challenge = self._make_fail_challenge()
        string_format = json.dumps({'success': success, 'gt':self.captcha_id ,'challenge': challenge})
        return string_format

    def _register_challenge(self):
        register_url = "{api_url}{handler}?gt={captcha_ID}".format(
            api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id)
        try:
            res_string = urllib2.urlopen(register_url, timeout=2).read()
        except:
            res_string = ""
        return res_string

    def validate(self, status, challenge, validate, seccode):
        """
        validate二次验证. `validate` 会根据 `status` 自动判断调用 `success_validat` 或者 `failback_validate`
        """
        if status:
            return self.success_validate(challenge, validate, seccode)
        else:
            return self.failback_validate(challenge, validate, seccode)

    def success_validate(self, challenge, validate, seccode):
        """
        正常模式的二次验证方式.向geetest server 请求验证结果.
        """
        if not self._check_para(challenge, validate, seccode):
            return self.FAIL_RES
        if not self._check_result(challenge, validate):
            return self.FAIL_RES
        validate_url =  "{api_url}{handler}".format(
            api_url=self.API_URL, handler=self.VALIDATE_HANDLER)
        query = {
            "seccode": seccode,
            "sdk": "python_%s" % self.sdk_version
        }
        query = urlencode(query)
        backinfo = self._post_values(validate_url, query)
        if backinfo == self._md5_encode(seccode):
            return self.SUCCESS_RES
        else:
            return self.FAIL_RES


    def _post_values(self, apiserver, data):
        req = urllib2.Request(apiserver)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        backinfo = response.read()
        return backinfo

    def _check_result(self, origin, validate):
        encodeStr = self._md5_encode(self.private_key + "geetest" + origin)
        if validate == encodeStr:
            return True
        else:
            return False

    def failback_validate(self, challenge, validate, seccode):
        """
        failback模式的二次验证方式.在本地对轨迹进行简单的判断返回验证结果.
        """
        if not self._check_para(challenge, validate, seccode):
            return self.FAIL_RES
        validate_str = validate.split('_')
        encode_ans = validate_str[0]
        encode_fbii = validate_str[1]      #_fbii : Full Bg Img Index
        encode_igi = validate_str[2]
        decode_ans = self.decode_response(challenge, encode_ans)
        decode_fbii = self.decode_response(challenge, encode_fbii)
        decode_igi = self.decode_response(challenge, encode_igi)  #_igi : Img Grp Index
        validate_result = self._validate_fail_image(decode_ans, decode_fbii, decode_igi)
        return validate_result

    def _check_para(self, challenge, validate, seccode):
        return bool(challenge.strip()) and bool(validate.strip()) and  bool(seccode.strip())

    def _validate_fail_image(self, ans, full_bg_index , img_grp_index):
        thread = 3
        full_bg_name = str(self._md5_encode(str(full_bg_index)))[0:10]
        bg_name = str(self._md5_encode(str(img_grp_index)))[10:20]
        answer_decode = ""
        for i in range(0,9):
            if i % 2 == 0:
                answer_decode += full_bg_name[i]
            elif i % 2 == 1:
                answer_decode += bg_name[i]
        x_decode = answer_decode[4:]
        x_int = int(x_decode, 16)
        result = x_int % 200
        if result < 40:
            result = 40
        if abs(ans - result) < thread:
            return self.SUCCESS_RES
        else:
            return self.FAIL_RES

    def _md5_encode(self, values):
        m = md5()
        m.update(values)
        return m.hexdigest()

    def _decode_rand_base(self, challenge):
        str_base = challenge[32:]
        i = 0
        temp_array = []
        for i in xrange(len(str_base)):
            temp_char = str_base[i]
            temp_ascii = ord(temp_char)
            result = temp_ascii - 87 if temp_ascii > 57 else temp_ascii - 48
            temp_array.append(result)
        decode_res = temp_array[0]*36 + temp_array[1]
        return decode_res

    def _decode_response(self, challenge, userresponse):
        if len(userresponse) > 100:
            return 0
        shuzi = (1, 2, 5, 10, 50)
        chongfu = set()
        key = {}
        count = 0
        for i in challenge:
            if i in chongfu:
                continue
            else:
                value = shuzi[count % 5]
                chongfu.add(i)
                count += 1
                key.update({i: value})
        res = 0
        for i in userresponse:
            res += key.get(i, 0)
        res = res - self._decode_rand_base(challenge)
        return res
