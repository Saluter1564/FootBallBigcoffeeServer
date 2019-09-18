"""newsapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from . import settings
import article.views as views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view
import article.views0 as views0

schema_view = get_swagger_view(title='足球大咖 API')
# 建立一个路由器对象
router = DefaultRouter(trailing_slash=False)
# 将我们的路由注册到url里
router.register(r'category', views.CategoryViewset, base_name="category")
router.register(r'categoryitems', views.CategoryitemsViewset, base_name="categoryitems")
router.register(r'categoryStringitems', views.CategoryStringitemsViewset, base_name="categoryStringitems")
router.register(r'categoryPrimaryKeyitems', views.CategoryPrimaryKeyitemsViewset, base_name="categoryPrimaryKeyitems")
router.register(r'categorySlugitems', views.CategorySlugitemsViewset, base_name="categorySlugitems")
router.register(r'item', views.ItemViewset, base_name="item")
router.register(r'tag', views.TagViewset, base_name="tag")
router.register(r'ad', views.AdViewset, base_name="ad")
router.register(r'articleList', views.ArticleListViewSet, base_name="articleList")
router.register(r'hot_articleList', views.Hot_articleListViewSet, base_name="hot_articleList")
router.register(r'user', views.UserViewset, base_name="user")
router.register(r'userFav', views.UserFavViewset, base_name="userFav")
router.register(r'userLogin', views.UserLoginViewset, base_name="userLogin")
router.register(r'setPassword', views.UserSetPasswordViewset, base_name="setPassword")
router.register(r'ttyingqiu', views.TtYingQiu, base_name="ttyingqiu")
router.register(r'test', views.test, base_name="test")
router.register(r'getMatchListByDate', views.getMatchListByDate, base_name='getMatchListByDate')
urlpatterns = [
    re_path('^$', schema_view),
    path('admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    re_path(r'login/', views.UserLogin.as_view(), name="login"),

]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
