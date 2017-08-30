from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import MainView, post, random, ItemListView, ItemView, UpdateItemView, DeleteItemView, CreateItemView


urlpatterns = [
    url(r'^$', MainView.as_view(), name='frostgrave_main'),
    url(r'^post/$', post, name='mass_upload'),
    url(r'^random-treasure/$', random, name='random_treasure'),
    url(r'^(?P<item>[A-Z-a-z]+)/$', ItemListView.as_view(), name='items'),
    url(r'^(?P<item_detail>[A-Z-a-z]+)/(?P<pk>\d+)$', ItemView.as_view(), name='item'),
    url(r'^(?P<item_edit>[A-Z-a-z]+)/(?P<pk>\d+)/edit$', UpdateItemView.as_view(), name='edit_item'),
    url(r'^(?P<item_delete>[A-Z-a-z]+)/(?P<pk>\d+)/delete$', DeleteItemView.as_view(), name='delete_item'),
    url(r'^(?P<item_create>[A-Z-a-z]+)/create$', CreateItemView.as_view(), name='create_item'),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
