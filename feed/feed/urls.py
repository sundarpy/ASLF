from django.conf.urls import url, include
from django.contrib import admin
from appes import views
from appes.views import HomeView, MyfeedView, FacetedSearchView, autocomplete
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^myfeed/(?P<slug>[-\w]+)/$', MyfeedView.as_view(), name='myfeed'),
    url(r'^search/autocomplete/$', autocomplete),
    url(r'^find/', FacetedSearchView.as_view(), name='haystack_search'),

    url(r'^feed_list/', views.feed_list, name='feed_list'),
    url(r'^new$', views.feed_create, name='feed_new'),
    url(r'^edit/(?P<pk>\d+)$', views.feed_update, name='feed_edit'),
  	url(r'^delete/(?P<pk>\d+)$', views.feed_delete, name='feed_delete'),

  	# url(r'url_view/', views.url_view, name="url_view" )
    
] + static(MEDIA_URL, document_root=MEDIA_ROOT)	