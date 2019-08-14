from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from server.inventory.views import LibraryView
from server.inventory import views as inventoryviews
from server.carts import views as cartsviews
from server.users import views as usersviews
# from server.accounts import views as accountsviews
from server import views

from django.views.static import serve
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
# 用户接口
router.register(r'users', usersviews.UserViewset, base_name="users")
# 短信验证码接口
router.register(r'codes', usersviews.SmsCodeViewset, base_name="codes")

urlpatterns = [
    url(r'^', include(router.urls)),
# 图片验证码
    url(r'^imagecode', usersviews.ImageCodeView.as_view(), name='imagename'),
# 访问图片URL
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # url(r'^account/$', accountsviews.AccountHomeView.as_view(), name='account' ),
    url(r'^library/$', inventoryviews.LibraryView.as_view(), name='library' ),
    url(r'^upload-document/$', inventoryviews.upload_form_view, name='upload-document'),
    url(r'^cart/update/$', cartsviews.cart_update, name='update-cart'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
