import hashlib
from datetime import datetime
import dateutil.relativedelta
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from . import models


# from rest_framework.token_authentication.settings import SECRET_KEY


# 基于token的用户认证
class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 1. 在请求头的query_params中获取token
        # token = request.query_params.get('token')

        # 2. 直接在请求头中获取token
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.user, token_obj)
            else:
                raise exceptions.AuthenticationFailed("用户token过期,请重新登录")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(username + str(time.time()), encoding='utf-8'))
    return m.hexdigest()


# 用户登录接口
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
            if user_obj:
                # 为登录用户创建token
                token = md5(username)
                # 保存(存在就更新不存在就创建，并设置过期时间为5分钟)
                expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(minutes=60)
                print(expiration_time, type(expiration_time))
                defaults = {
                    "token": token,
                    "expiration_time": expiration_time
                }
                models.UserToken.objects.update_or_create(user=user_obj, defaults=defaults)
                return Response({"code": 200, "token": token})
            else:
                return Response({"code": 401, "error": "用户名或密码错误"})
        except Exception as e:
            print(e)
            return Response({"code": 500, "error": "用户名或密码错误"})


# 商品接口
class GoodsView(APIView):
    authentication_classes = [TokenAuthtication, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        try:
            goods_data_list = [
                {'id': 1, 'goods_name': "草莓", 'price': 19.99, 'status': True},
                {'id': 2, 'goods_name': "香蕉", 'price': 9.88, 'status': True},
                {'id': 3, 'goods_name': "苹果", 'price': 5.99, 'status': True},
                {'id': 4, 'goods_name': "蓝莓", 'price': 9.99, 'status': True},
            ]
            return Response({"code": 200, "msg": "商品接口", "data_list": goods_data_list})
        except Exception as e:
            print(e)
            return Response({"code": 500, "error": "接口维护中..."})


# 用户信息接口
class UserInfoView(APIView):
    authentication_classes = [TokenAuthtication, ]

    def get(self, request, *args, **kwargs):
        try:
            username = request.user
            user_obj = models.UserInfo.objects.filter(username=username).first()
            data = {}
            data["username"] = user_obj.username
            data["user_type"] = user_obj.user_type
            data["add_time"] = user_obj.add_time
            return Response({"code": 200, "msg": "用户信息接口", "userinfo": data})
        except Exception as e:
            print(e)
            return Response({"code": 500, "error": "接口维护中..."})

    def post(self, request, *args, **kwargs):
        try:
            token = request.data["token"]
            token_obj = models.UserToken.objects.filter(token=token).first()
            if token_obj:

                models.UserInfo.objects.get(username=token_obj)
                return Response({"code": 200, "username": token})
            else:
                return Response({"code": 401, "error": "token错误"})
        except Exception as e:
            print(e)
            return Response({"code": 500, "error": "token错误"})
