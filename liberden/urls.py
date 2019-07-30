from django.contrib import admin
from django.conf.urls import url, include
from server.inventory.views import LibraryView
from server.inventory import views

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='Libray' ),
    url(r'^upload/$', views.model_form_upload, name='Upload'),
    url(r'^admin/', admin.site.urls)
]
