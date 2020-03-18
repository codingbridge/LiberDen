# pylint: disable=missing-docstring
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from server.inventory import views as inventoryviews
from server.carts import views as cartsviews
from server.users import views as usersviews
from server.readerpoints import views as readerviews
from server import views


# from django.views.static import serve
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# 用户接口
# router.register(r'users', usersviews.UserViewset, base_name="users")
# 短信验证码接口
# router.register(r'codes', usersviews.SmsCodeViewset, base_name="codes")

urlpatterns = [
    # url(r'^', include(router.urls)),
    # 图片验证码
    # url(r'^imagecode', usersviews.ImageCodeView.as_view(), name='imagename'),
    # 访问图片URL
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^signup/$', usersviews.signup_view, name='signup'),
    url(r'^login/$', usersviews.signin_view, name='login'),
    url(r'^logout/$', usersviews.logout_view, name='logout'),
    url(r'^settings/$', usersviews.edituser_view, name='settings'),
    url(r'^password/$', usersviews.changepassword_view, name='changepassword'),
    url(r'^forgotpassword/$', usersviews.forgotpassword_view, name='forgotpassword'),
    url(r'^resetpassword/<uidb64>/<token>/$', usersviews.resetpassword_view, name='resetpassword'),
    url(r'^myborrowing/$', readerviews.myborrowing_view, name='myborrowing'),
    url(r'^pointscard/$', readerviews.pointscard_view, name='pointscard'),
    url(r'^book/$', inventoryviews.book_add_view, name='book'),
    url(r'^inventory/$', inventoryviews.inventory_add_view, name='inventory'),
    url(r'^library/$', inventoryviews.inventory_page_view, name='library'),
    url(r'^upload-document/$', inventoryviews.upload_form_view, name='upload-document'),
    url(r'^cart/update/$', cartsviews.cart_update, name='update-cart'),
    url(r'^cart/clear/$', cartsviews.cart_clear, name='clear-cart'),
    url(r'^cart/checkout/$', cartsviews.cart_checkout, name='checkout-cart'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^cart/$', cartsviews.cart_view, name="cart"),
    url(r'^admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
