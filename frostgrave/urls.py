from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import MainView, post, random



urlpatterns = [
    url(r'^$', MainView.as_view(), name='frostgrave_main'),
    url(r'^post/$', post, name='mass_upload'),
    url(r'^random-treasure/$', random, name='random_treasure'),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
