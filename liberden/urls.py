from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from server.inventory.views import LibraryView
from server.inventory import views as inventoryviews
from server.carts import views as cartsviews
from server import views

urlpatterns = [
    url(r'^library/$', inventoryviews.LibraryView.as_view(), name='library' ),
    # url(r'^library/category/<category>/', inventoryviews.LibraryView.as_view(), name='library' ),
    url(r'^upload-document/$', inventoryviews.upload_form_view, name='upload-document'),
    url(r'^cart/update/$', cartsviews.cart_update, name='update-cart'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
