from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    url(r'recommendations/$', views.get_recommendations, name='get_recommendations'),
    url(r'search/$', views.search, name='search'),
    url(r'^$', views.index, name='index')
]   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 