#GeeTest-Python-SDK

###安装过程：

1\. 下载SDK，并将geetest.py放入相应的路径  
2\. 在需要调用验证码的文件头中调用geetest，并用获取的PRIVATE-KEY作为第一个参数实例化：  
```python
import geetest
gt=geetest.geetest("0f1a37e33c9ed10dd2e133fe2ae9c459")
```
3\. 从客户端的post请求中获取`geetest_challenge`，`geetest_validate`，`geetest_seccode`三个字段。  
```python
challenge=i.geetest_challenge
validate=i.geetest_validate
seccode=i.geetest_seccode
```
4\. 使用`gt.geetest_validate`进行验证，依次传入 `challenge`,`validate`,`seccode`参数，此函数在验证通过时返回1，失败时返回0  
```python
if gt.geetest_validate(challenge,validate,seccode):
    return "OK"
else:
    return "false"
```
###注意事项  
`geetest.py`模块在验证时会调用`urllib2`访问`http://api.geetest.com/validate.php`进行验证  
###依赖  
`urllib2`
`time`
`hashlib`
###实例  
见demo文件夹