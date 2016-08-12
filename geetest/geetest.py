#!coding:utf8
import sys
import random
import json
import requests
import time
from hashlib import md5


if sys.version_info >= (3,):
    xrange = range    

VERSION = "3.2.0"


class GeetestLib(object):

    FN_CHALLENGE = "geetest_challenge"
    FN_VALIDATE = "geetest_validate"
    FN_SECCODE = "geetest_seccode"

    GT_STATUS_SESSION_KEY = "gt_server_status"

    API_URL = "http://api.geetest.com"
    REGISTER_HANDLER = "/register.php"
    VALIDATE_HANDLER = "/validate.php"

    def __init__(self, captcha_id, private_key):
        self.private_key = private_key
        self.captcha_id = captcha_id
        self.sdk_version = VERSION
        self._response_str = ""

    def pre_process(self, user_id=None):
        """
        验证初始化预处理.
        """
        status, challenge = self._register(user_id)
        self._response_str = self._make_response_format(status, challenge)
        return status

    def _register(self, user_id=None):
        challenge = self._register_challenge(user_id)
        if len(challenge) == 32:
            challenge = self._md5_encode("".join([challenge, self.private_key]))
            return 1, challenge
        else:
            return 0, self._make_fail_challenge()

    def get_response_str(self):
        return self._response_str

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
        string_format = json.dumps(
            {'success': success, 'gt':self.captcha_id, 'challenge': challenge})
        return string_format

    def _register_challenge(self, user_id=None):
        if user_id:
            register_url = "{api_url}{handler}?gt={captcha_ID}&user_id={user_id}".format(
                api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id, user_id=user_id)
        else:
            register_url = "{api_url}{handler}?gt={captcha_ID}".format(
                api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id)
        try:
            response = requests.get(register_url, timeout=2)
            if response.status_code == requests.codes.ok:
                res_string = response.text
            else:
                res_string = ""
        except:
            res_string = ""
        return res_string

    def success_validate(self, challenge, validate, seccode, user_id=None,gt=None,data='',userinfo=''):
        """
        正常模式的二次验证方式.向geetest server 请求验证结果.
        """
        if not self._check_para(challenge, validate, seccode):
            return 0
        if not self._check_result(challenge, validate):
            return 0
        validate_url = "{api_url}{handler}".format(
            api_url=self.API_URL, handler=self.VALIDATE_HANDLER)
        query = {
            "seccode": seccode,
            "sdk": ''.join( ["python_",self.sdk_version]),
            "user_id": user_id,
            "data":data,
            "timestamp":time.time(),
            "challenge":challenge,
            "userinfo":userinfo,
            "captchaid":gt
        }
        backinfo = self._post_values(validate_url, query)
        if backinfo == self._md5_encode(seccode):
            return 1
        else:
            return 0

    def _post_values(self, apiserver, data):
        response = requests.post(apiserver, data)
        return response.text

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
            return 0
        validate_str = validate.split('_')
        encode_ans = validate_str[0]
        encode_fbii = validate_str[1]
        encode_igi = validate_str[2]
        decode_ans = self._decode_response(challenge, encode_ans)
        decode_fbii = self._decode_response(challenge, encode_fbii)
        decode_igi = self._decode_response(challenge, encode_igi)
        validate_result = self._validate_fail_image(
            decode_ans, decode_fbii, decode_igi)
        return validate_result

    def _check_para(self, challenge, validate, seccode):
        return (bool(challenge.strip()) and bool(validate.strip()) and  bool(seccode.strip()))

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
            return 1
        else:
            return 0

    def _md5_encode(self, values):
        if type(values) == str:
            values = values.encode()
        m = md5(values)
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
