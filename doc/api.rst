API
===========
.. contents::

API提供的类:  GeetestLib

主要方法有  :	pre_process(); post_validate(); failback_validate().

初始化
----------------
在调用GeetestLib前请自行设定公钥和私钥：

 .. code-block :: python

	captach_id = "你的公钥"
	private_key = "你的私钥"
	gt = GeetestLib(captach_id, private_key)


GeetestLib 
-----------------
.. automodule:: python_sdk.geetest
    :members:
    :undoc-members:
    :show-inheritance:
