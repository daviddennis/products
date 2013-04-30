from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('products.views',
    url(r'^cars$', 'cars'),
    url(r'^cars/(?P<pk>\d+)$', 'cars'),
    url(r'^cars/add$', 'cars_add'),    
    url(r'^furniture$', 'furniture'),
    url(r'^furniture/(?P<pk>\d+)$', 'furniture'),
    url(r'^holograms$', 'holograms'),
    url(r'^holograms/(?P<pk>\d+)$', 'holograms'),
    url(r'^audiobooks$', 'audiobooks'),
    url(r'^audiobooks/(?P<pk>\d+)$', 'audiobooks'),
    url(r'^admin/', include(admin.site.urls)),
)
