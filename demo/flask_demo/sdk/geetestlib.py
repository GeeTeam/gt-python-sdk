#!coding:utf8
from hashlib import md5
import string
import urllib2
import random
import json
# SDK_version = "2.0.0"
# Python_version = 2.7.6

class GeetestLib(object):

    def __init__(self, id, key):
        self.private_key = key                    #私钥
        self.captcha_ID = id                      #公钥
        self.sdk_version = "2.0.0"                #SDK版本
        self.challenge = ""

        self.base_url = "api.geetest.com"
        self.api_url = "http://" + self.base_url  #HTTPS API URL
        self.host = self.api_url
        self.host_port = 80                       #API 接口

        self.success_res = "success"              #验证返还成功结果
        self.fail_res = "fail"                    #验证返还失败结果

        self.fn_challenge = "geetest_challenge"   #二次验证表单数据challenge
        self.fn_validate = "geetest_validate"     #二次验证表单数据validate
        self.fn_seccode = "geetest_seccode"       ##二次验证表单数据seccode

    def pre_process(self):
        """
        验证初始化预处理，包括register().

        :return Boolean:
        """
        if self.register():
            return True
        else:
            return False

    def register(self):
        """
        验证初始化.

        :return Boolean:
        """
        path = "/register.php"
        host = self.host
        if self.captcha_ID == None:
            return False
        else:
            challenge=self.register_challenge()
            if len(challenge) == 32:
                self.challenge = challenge
                return True
            else:
                return False

    def fail_pre_process(self):
        """
        预处理失败后的返回格式串.

        :return Json字符串:
        """
        rnd1 = int(round(random.random()*100))
        rnd2 = int(round(random.random()*100))
        md5_str1 = self.md5_encode(str(rnd1))
        md5_str2 = self.md5_encode(str(rnd2))
        challenge = md5_str1 + md5_str2[0:2]
        string_format = json.dumps({'success': 0, 'gt':self.captcha_ID ,'challenge': self.challenge})
        return string_format

    def success_pre_process(self):
        """
        预处理成功后的标准串

        :return Json字符串:
        """
        string_format = json.dumps({'success': 1, 'gt':self.captcha_ID ,'challenge': self.challenge})
        return string_format

    def register_challenge(self):
        """
        challange获取url.

        :return res_string:
        """
        api_reg = "http://api.geetest.com/register.php?"
        reg_url = api_reg + "gt=%s"%self.captcha_ID
        try:
            res_string = urllib2.urlopen(reg_url, timeout=2).read()
        except:
            res_string = ""
        return res_string

    def post_validate(self, challenge, validate, seccode):
        """
        validate二次验证.

        :param challenge:
        :param validate:
        :param seccode:
        :return result:
        """
        apiserver = "http://api.geetest.com/validate.php"
        if validate == self.md5_encode(self.private_key + 'geetest' + challenge):
            query = 'seccode=' + seccode + "&sdk=python_" + self.sdk_version
            backinfo = self.post_values(apiserver, query)
            if backinfo == self.md5_encode(seccode):
                return self.success_res
            else:
                return self.fail_res
        return self.fail_res

    def post_values(self, apiserver, data):
        """
        向gt-server发起二次验证请求.

        :param apiserver:
        :param data:
        :return backinfo:
        """
        req = urllib2.Request(apiserver)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        backinfo = response.read()
        return backinfo

    def check_result(self, origin, validate):
        """
        二次验证先验判断，判断validate是否与privatekey,challenge 吻合

        :param origin:
        :param validate:
        :returns Boolean:
        """
        encodeStr = self.md5_encode(self.private_key + "geetest" + origin)
        if validate == encodeStr:
            return True
        else:
            return False

    def failback_validate(self, challenge, validate, seccode):
        """
        failback模式的验证方式,验证结果

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

    def request_is_legal(self, challenge, validate, seccode):
        """
        判断请求是否合法

        :return Boolean:
        """
        if bool(challenge.strip()) and bool(validate.strip()) and  bool(seccode.strip()):
            return True
        else :
            return False

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

    def set_gtserver_session(self, set_func, status_code, challenge):
        """
       设置gt-server状态值session

       :param set_func:
       :param status_code:
        """
        set_func('gt_server_status', status_code)
        set_func('gt_challenge', challenge)

    def  get_gtserver_session(self, get_func, key):
        """
        获取gt-server状态值session 

        :param get_func:
        :return status_code:
        """
        if key == 'gt_server_status':
            status_code = int(get_func('gt_server_status'))
            return status_code
        if key == 'gt_challenge':
            challenge = get_func('gt_challenge')
            return challenge
        else:
            return False

    def md5_encode(self, values):
        """
        md5编码

        :param values: 
        :return md5:
        """
        import hashlib
        m = hashlib.md5()
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







