#!coding:utf8
import string
import urllib2
import random
import json
from hashlib import md5
from urllib import urlencode


VERSION = "3.0.0dev1"


class GeetestLib(object):

    FN_CHALLENGE = "geetest_challenge"
    FN_VALIDATE = "geetest_validate" 
    FN_SECCODE = "geetest_seccode" 

    SUCCESS_RES = "success" 
    FAIL_RES = "fail" 

    API_URL = "http://api.geetest.com" 
    REGISTER_HANDLER = "/register.php"
    VALIDATE_HANDLER = "/validate.php"


    def __init__(self, id, key):
        self.private_key = key                    #私钥
        self.captcha_id = id                      #公钥
        self.sdk_version = VERSION              #SDK版本

    def pre_process(self):
        """
        验证初始化预处理.

        :return Boolean:
        """
        status, challenge = self._register()

    def _register(self):
        challenge=self._register_challenge()
        if len(challenge) == 32:
            return 1, challenge
        else:
            return 0, self._make_fail_challenge()

    def _make_fail_challenge(self):
        rnd1 = int(round(random.random()*100))
        rnd2 = int(round(random.random()*100))
        md5_str1 = self.md5_encode(str(rnd1))
        md5_str2 = self.md5_encode(str(rnd2))
        challenge = md5_str1 + md5_str2[0:2]
        return challenge

    def _make_response_format(self, success=1, challenge=None):
        if not challenge:
            challenge = self._make_fail_challenge()
        string_format = json.dumps({'success': success, 'gt':self.captcha_ID ,'challenge': challenge})
        return string_format

    def _register_challenge(self):
        register_url = "{api_url}{handler}?gt={captcha_ID}".format(
            api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id)
        try:
            res_string = urllib2.urlopen(register_url, timeout=2).read()
        except:
            res_string = ""
        return res_string

    def post_validate(self, status, challenge, validate, seccode):
        """
        validate二次验证.

        :param challenge:
        :param validate:
        :param seccode:
        :return result:
        """
        if status:
            return self.success_validate(challenge, validate, seccode)
        else:
            return self.failback_validate(challenge, validate, seccode)

    def success_validate(self, challenge, validate, seccode):
        """
        正常模式的二次验证方式

        :param challenge:
        :param validate:
        :param seccode:
        :return result:
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
        if backinfo == self.md5_encode(seccode):
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
        encodeStr = self.md5_encode(self.private_key + "geetest" + origin)
        if validate == encodeStr:
            return True
        else:
            return False

    def failback_validate(self, challenge, validate, seccode):
        """
        failback模式的二次验证方式

        :param challenge:
        :param validate:
        :param seccode:
        :return result:
        """
        if not self.request_is_legal(challenge, validate, seccode):
            return self.fail_res
        validate_str = "".join(validate.split('_'))
        encode_ans = validate_str[0]
        encode_fbii = validate_str[1]      #_fbii : Full Bg Img Index
        encode_igi = validate_str[2]
        decode_ans = self.decode_response(self.challenge, encode_ans)
        decode_fbii = self.decode_response(self.challenge, encode_fbii)
        decode_igi = self.decode_response(self.challenge, encode_igi)  #_igi : Img Grp Index
        validate_result = self.validate_fail_image(decode_ans, decode_fbii, decode_igi)
        if not validate_result == self.fail_res:
            rand1 = self.random_num()
            md5Str = self.md5_encode(rand1 + "")
            self.challenge = md5Str
        return validate_result

    def _check_para(self, challenge, validate, seccode):
        return bool(challenge.strip()) and bool(validate.strip()) and  bool(seccode.strip())

    def validate_fail_image(self, ans, full_bg_index , img_grp_index):
        """
        failback模式下，简单判断轨迹是否通过

        :param ans:
        :param full_bg_index:
        :param img_grp_index:
        :return result:
        """
        thread = 3
        full_bg_name = str(self.md5_encode(str(full_bg_index)))[0:10]
        bg_name = str(self.md5_encode(str(img_grp_index)))[0:10]
        answer_decode = ""
        for i in range(0,9):
            if i % 2 == 0:
                answer_decode += full_bg_name[i]
            elif i % 2 == 1:
                answer_decode += bg_name[i]
        x_decode = answer_decode[4]
        x_int = string.atoi(x_decode, 16)
        result = x_int % 200
        if result < 40:
            result = 40
        if abs(ans - result) < thread:
            return self.success_res
        else:
            return self.fail_res

    def md5_encode(self, values):
        """
        md5编码

        :param values:
        :return md5:
        """
        m = md5()
        m.update(values)
        return m.hexdigest()

    def decode_rand_base(self, challenge):
        """
        输入的两位的随机数字,解码出偏移量

        :param challenge:
        :return decode_result:
        """
        str_base = challenge[32:34]
        i = 0
        temp_array = []
        while i < len(str_base):
            temp_char = str_base[i]
            temp_Ascii = ord(temp_char)
            result = temp_Ascii - 87 if temp_Ascii > 57 else temp_Ascii - 48
            temp_array.append(result)
            i += 1
        decode_res = temp_array[1]*36 + temp_array[1]
        return decode_res

    def decode_response(self, challenge, userresponse):
        """
        response解码

        :param challenge:
        :param userresponse:
        :return decode_result:
        """
        if len(userresponse) > 100:
            return 0
        shuzi = (1, 2, 5, 10, 50)
        chongfu = []
        key = {}
        count = 0
        for i in challenge:
            if i in chongfu:
                continue
            else:
                value = shuzi[count % 5]
                chongfu.append(i)
                count += 1
                key.update({i: value})
        res = 0
        for i in userresponse:
            res += key.get(i, 0)
        return res

    def random_num():
        """
        随机数生成

        :return Float:
        """
        rand_num = random.random()*100
        return rand_num







