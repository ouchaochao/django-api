from django.conf.urls import url
from api import views

urlpatterns = [
    # 用户登录接口
    url(r'login/$', views.LoginView.as_view()),

    # 商品列表接口
    url(r'goods/$', views.GoodsView.as_view()),

    # 用户信息接口
    url(r'userinfo/$', views.UserInfoView.as_view()),
]
