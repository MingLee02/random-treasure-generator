from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import MainView, post, random
from .trinketViews import CreateTrinketView, TrinketView, TrinketListView, UpdateTrinketView, DeleteTrinketView



urlpatterns = [
    url(r'^$', MainView.as_view(), name='frostgrave_main'),
    url(r'^post/$', post, name='mass_upload'),
    url(r'^random-treasure/$', random, name='random_treasure'),
    url(r'^trinkets/$', TrinketListView.as_view(), name='frostgrave_trinkets'),
    url(r'^trinket/create$', CreateTrinketView.as_view(), name='create_trinket'),
    url(r'^trinket/(?P<pk>\d+)$', TrinketView.as_view(), name='frostgrave_trinket'),
    url(r'^trinket/(?P<pk>\d+)/edit$', UpdateTrinketView.as_view(), name='edit_trinket'),
    url(r'^trinket/(?P<pk>\d+)/delete$', DeleteTrinketView.as_view(), name='delete_trinket'),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
