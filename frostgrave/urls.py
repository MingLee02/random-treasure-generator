from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import MainView, UploadSheetView, post, random, ItemListView, ItemView, UpdateItemView, DeleteItemView, CreateItemView, search


urlpatterns = [
    re_path(r'^$', MainView.as_view(), name='frostgrave_main'),
    re_path(r'^upload-sheet/$', UploadSheetView.as_view(), name='frostgrave_upload_sheet'),
    re_path(r'^post/$', post, name='mass_upload'),
    re_path(r'^search/$', search, name='search_data'),
    re_path(r'^random-treasure/$', random, name='random_treasure'),
    re_path(r'^(?P<item>[A-Z-a-z]+)/$', ItemListView.as_view(), name='items'),
    re_path(r'^(?P<item_detail>[A-Z-a-z]+)/(?P<pk>\d+)$', ItemView.as_view(), name='item'),
    re_path(r'^(?P<item_edit>[A-Z-a-z]+)/(?P<pk>\d+)/edit$', UpdateItemView.as_view(), name='edit_item'),
    re_path(r'^(?P<item_delete>[A-Z-a-z]+)/(?P<pk>\d+)/delete$', DeleteItemView.as_view(), name='delete_item'),
    re_path(r'^(?P<item_create>[A-Z-a-z]+)/create$', CreateItemView.as_view(), name='create_item'),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
