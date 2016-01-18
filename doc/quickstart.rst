快速开始
==========

下面使用示例代码的均以flask框架为例.

获取代码
---------------

从 `Github <https://github.com/GeeTeam/gt-python-sdk/>`__ 上Clone代码:

.. code-block:: bash

    $ git clone https://github.com/GeeTeam/gt-python-sdk.git

安装GeetestSDK
----------------------------------
.. code-block:: bash

    $ sudo python setup.py install

初始化验证
----------------
在调用GeetestLib前请自行设定公钥和私钥：

.. code-block :: python

  captach_id = "你的公钥"
  private_key = "你的私钥"

根据自己的私钥出初始化验证

.. code-block :: python

  @app.route('/getcaptcha', methods=["GET"])
  def get_captcha():
      gt = GeetestLib(captach_id, private_key)
      status, response_str = gt.pre_process()
      session[gt.GT_STATUS_SESSION_KEY] = gt
      return response_str

上述代码是一般验证初始化的代码,因为现在我们服务提供完备的服务宕机方案,所以推荐直接使用我们的宕机方案,也可以换成你们自己的方案,根据返回的`status` 自行处理.

二次验证
-----------

.. code-block :: python

  @app.route('/validate', methods=["POST"])
  def validate_capthca():
      gt = GeetestLib(captcha_id, private_key)
      status = session[gt.GT_STATUS_SESSION_KEY]
      challenge = request.form[gt.FN_CHALLENGE]
      validate = request.form[gt.FN_VALIDATE]
      seccode = request.form[gt.FN_SECCODE]
      gt = GeetestLib(captcha_id, private_key)
      result = gt.validate(status, challenge, validate, seccode)
      return result

如果不想采用极验提供的failback方案,你可以自己处理，代码如下

.. code-block :: python

  @app.route('/validate', methods=["POST"])
  def validate_capthca():
      status = session[GeetestLib.GT_STATUS_SESSION_KEY]
      if status:
          gt = GeetestLib(captcha_id, private_key)
          challenge = request.form[gt.FN_CHALLENGE]
          validate = request.form[gt.FN_VALIDATE]
          seccode = request.form[gt.FN_SECCODE]
          result = gt.success_validat(challenge, validate, seccode)
      else:
          #你们自己的验证方法
      return result

运行demo
---------------

Django demo运行
^^^^^^^^^^^^^^^^^^^^^^^^^

进入django_demo文件夹，运行:

.. code-block:: bash

    $ python manage.py runserver 0.0.0.0:8000

在浏览器中访问http://localhost:8000即可看到Demo界面

Flask demo运行
^^^^^^^^^^^^^^^^^^^^^^^^^

进入flask_demo文件夹，运行：

.. code-block:: bash

    $ python start.py


在浏览器中访问http://localhost:5000即可看到Demo界面

Tornado demo运行
^^^^^^^^^^^^^^^^^^^^^^^^^
进入tornado_demo文件夹，运行:

.. code-block:: bash

    $ python app.py

在浏览器中访问http://localhost:8088即可看到Demo界面
