#GeeTest-Python-SDK

##文件描述

1. *geetest.py*
 
      极验的PythonSDK

2. *django_demo*
    
       django项目demo文件


##运行django demo
1. 从GitHub中clone一份到本地
2. 进入django_demo文件夹
3. 运行 
          
         python manage.py runserver 0.0.0.0:8000
        
4. 在浏览器中访问http://localhost:8000即可看到Demo界面                
        
 
##SDK 使用说明
###1.Init with private key and captcha id 使用私钥和公钥初始化
         captcha_id ="Captcha Id"
         private_key = "Private Key"
###2.Use register api to get challenge on each request 在每次用户请求验证码时使用register接口获取challenge
        gt = geetest.geetest(captcha_id, private_key)
        challenge = gt.geetest_register()
###3.Use challenge 使用获取的challenge构造scr
        BASE_URL = "api.geetest.com/get.php?gt="
        if len(challenge) == 32:
            url = "http://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
            httpsurl = "https://%s%s&challenge=%s" % (BASE_URL, captcha_id, challenge)
        return render_to_response("index.html", {"url": url}, context_instance=RequestContext(request))    
###4.Add captcha script to your page 在页面上添加验证的script
        <div class="box">
                    {% if url %}
                    <script type="text/javascript" src="{{url}}"></script>
                    {% else %}
                    <p> please insert your local captcha system code! </p>
                    {% endif %}
         </div>
###Validate API 验证函数
        challenge = request.POST.get('geetest_challenge', '')
        validate = request.POST.get('geetest_validate', '')
        seccode = request.POST.get('geetest_seccode', '')
        gt = geetest.geetest(captcha_id, private_key)
        result = gt.geetest_validate(challenge, validate, seccode)
        if result:
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
         