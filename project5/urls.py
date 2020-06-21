from django.conf.urls import url, include
from api import views as api_views
from dj import views as dj_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', dj_views.UserViewSet)
router.register(r'groups', dj_views.GroupViewSet)

urlpatterns = [
    # 用户登录接口
    url(r'login/$', api_views.LoginView.as_view()),

    # 商品列表接口
    url(r'goods/$', api_views.GoodsView.as_view()),

    # 用户信息接口
    url(r'userinfo/$', api_views.UserInfoView.as_view()),

    # 使用自动URL路由连接我们的API。
    # 另外，我们还包括支持浏览器浏览API的登录URL。
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('snippets.urls')),

]
