from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from server.inventory.views import LibraryView
from server.inventory import views
from server.carts import views as cartsviews

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='libray' ),
    url(r'^upload/$', views.model_form_upload, name='upload'),
    url(r'^cart/update/$', cartsviews.cart_update, name='update'),
    # url(r'^updatecart$', views.update_cart, name='UpdateCart'),
    url(r'^admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
