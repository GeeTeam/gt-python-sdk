Gt Python SDK
===============
使用 3.1 之前版本SDK的用户如果想更新到3.1以及以后版本请先联系极验客服,因为为了兼容老用户,新的特性需要修改验证设置。

极验验证的Python SDK目前提供基于django, flask, tornado框架的DEMO。

本项目是面向服务器端的，具体使用可以参考我们的 `文档 <http://www.geetest.com/install/sections/idx-server-sdk.html>`_ ,客户端相关开发请参考我们的 `前端文档。 <http://www.geetest.com/install/>`_.

开发环境
----------------

 - Python (推荐2.7.0以上版本）
 - django, flask, tornado框架

快速开始
---------------

下面使用示例代码的均以flask框架为例。

1. 获取代码

从 `Github <https://github.com/GeeTeam/gt-python-sdk/>`__ 上Clone代码:

.. code-block:: bash

    $ git clone https://github.com/GeeTeam/gt-python-sdk.git

2. 安装GeetestSDK

.. code-block:: bash

    $ sudo python setup.py install

3. 初始化验证


在调用GeetestLib前请自行设定公钥和私钥,用户id为可选项，默认为随机数字：

.. code-block :: python

  captach_id = "你的公钥"
  private_key = "你的私钥"
  user_id = random.randint(1,100)

根据自己的私钥初始化验证

.. code-block :: python

  @app.route('/getcaptcha', methods=["GET"])
  def get_captcha():
      user_id = random.randint(1,100)
      gt =  GeetestLib(captcha_id, private_key)
      status = gt.pre_process(user_id)
      session[gt.GT_STATUS_SESSION_KEY] = status
      session["user_id"] = user_id
      response_str = gt.get_response_str()
      return response_str

4. 二次验证

.. code-block :: python

  @app.route('/validate', methods=["POST"])
  def validate_capthca():
      gt = GeetestLib(captcha_id, private_key)
      status = session[gt.GT_STATUS_SESSION_KEY]
      challenge = request.form[gt.FN_CHALLENGE]
      validate = request.form[gt.FN_VALIDATE]
      seccode = request.form[gt.FN_SECCODE]
      user_id = session["user_id"]
      if status:
          result = gt.success_validate(challenge, validate, seccode, user_id)
      else:
          result = gt.fail_validate(challenge, validate, seccode)
      result = "success" if result else "fail"
      return result


运行demo
---------------------

1. django demo运行：进入django_demo文件夹，运行：

.. code-block:: bash

    $ python manage.py runserver 0.0.0.0:8000

在浏览器中访问http://localhost:8000即可看到Demo界面

2. flask demo运行：进入flask_demo文件夹，运行：

.. code-block:: bash

    $ python start.py

在浏览器中访问http://localhost:5000即可看到Demo界面

3. tornado demo运行：进入tornado_demo文件夹，运行:

.. code-block:: bash

    $ python start.py

在浏览器中访问http://localhost:8088即可看到Demo界面


发布日志
-----------------
+ 3.2.0

 - 添加用户标识(user_id)的接口

+ 3.1.2

 - 支持Python3

+ 3.1.1

 - 统一接口

+ 3.1.0

 - 添加challenge加密特性，使验证更安全， 老版本更新请先联系管理员

+ 3.0.1

 - 修复failback情况下 无法正确解码答案的错误

+ 3.0.0

 - 去除SDK对Session操作， 现在Session部分由开发者自己处理
 - 简易化初始化过程.
 - 修复failback模式BUG
