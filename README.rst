Gt Python SDK
===============

极验验证的Python SDK目前提供基于django, flask, tornado框架的DEMO
本项目提供的Demo的前端实现方法均是面向PC端的。 如果需要移动端的canvas功能，请参考canvas的 `前端文档 <http://www.geetest.com/install/>`_.

开发环境
_______________

 - Python (推荐2.7.0以上版本）
 - django, flask, tornado框架

快速开始
_______________

1. 从 `Github <https://github.com/GeeTeam/gt-python-sdk/>`__ 上Clone代码:

.. code-block:: bash

    $ git clone https://github.com/GeeTeam/gt-python-sdk.git

2. django demo运行：进入django_demo文件夹，运行：

.. code-block:: bash

    $ python start.py runserver 0.0.0.0:8000  

在浏览器中访问http://localhost:8000即可看到Demo界面

3. flask demo运行：进入flask_demo文件夹，运行：

.. code-block:: bash

    $ python start.py

在浏览器中访问http://localhost:5000即可看到Demo界面
 
4. tornado demo运行：进入tornado_demo文件夹，运行:

.. code-block:: bash

    $ python start.py

在浏览器中访问http://localhost:8088即可看到Demo界面


SDK 使用说明
_________________

以django为例

1. 核心SDK库: ../python_sdk/geetest.py

2. api文档:  ../doc/api.rst

3. 公钥和私钥初始化：查看../demo/django_demo/app/views.py

.. code-block:: python

 captcha_id ="你的公钥"
 private_key = "你的私钥"

4. 请求验证码时使用register_challenge()获取challenge

.. code-block:: python

 gt = geetest.GeetestLib(captcha_id, private_key)
 challenge = gt.register_challenge()

5. 预处理和session控制

.. code-block:: python

 gt =  GeetestLib(captcha_id, private_key)
 if gt.pre_process():
     res_str = gt.success_pre_process()
     gt.set_gtserver_session(session.__setitem__, 1, gt.challenge)
 else:                   #宕机情况下提供failback方案，可自行更换
     res_str = gt.fail_pre_process()
     gt.set_gtserver_session(session.__setitem__, 0, gt.challenge)
 return res_str

6. validate验证：

.. code-block:: python

 if request.method == "POST":
     challenge = request.POST.get('geetest_challenge', '')
     validate = request.POST.get('geetest_validate', '')
     seccode = request.POST.get('geetest_seccode', '')
     gt = geetest.GeetestLib(captcha_id, private_key)
     gt_challenge = gt.get_gtserver_session(request.session.__getitem__, 'gt_challenge')
     gt_server_status = gt.get_gtserver_session(request.session.__getitem__, 'gt_server_status')
     if not gt_challenge == challenge[0:32]:
         return HttpResponse("fail")
     if gt_server_status == 1:
         result = gt.post_validate(challenge, validate, seccode)
     else:
         result = gt.failback_validate(challenge, validate, seccode)
     return HttpResponse(result)
 return HttpResponse("error")

发布日志
_______________
+[2.0.2]
 - 添加通过session的challenge验证
 - Date : 2015.12.30
+[2.0.1]
 - SDK库和django和flask demo重制
 - Date : 2015.12.24        
