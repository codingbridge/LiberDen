from django.contrib import admin
from django.conf.urls import url, include
from server.inventory.views import LibraryView


urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='Libray' ),
    url(r'^admin/', admin.site.urls)
]
