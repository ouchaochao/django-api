from django.conf.urls import url, include
from snippets import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')
# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# API URL现在由路由器自动确定。
# 另外，我们还要包含可浏览的API的登录URL。
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^schema/$', schema_view),
]
