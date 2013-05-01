from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('products.views',
    url(r'^$', 'show_products'),
    url(r'^cars$', 'cars'),
    url(r'^cars/(?P<pk>\d+)$', 'cars'),
    url(r'^cars/add/(?P<field_name>\w+)$', 'add_attribute'),    
    url(r'^cars/remove/(?P<field_name>\w+)$', 'remove_attribute'),    
    url(r'^furniture$', 'furniture'),
    url(r'^furniture/(?P<pk>\d+)$', 'furniture'),
    url(r'^furniture/add/(?P<field_name>\w+)$', 'add_attribute'),    
    url(r'^furniture/remove/(?P<field_name>\w+)$', 'remove_attribute'),    
    url(r'^holograms$', 'holograms'),
    url(r'^holograms/(?P<pk>\d+)$', 'holograms'),
    url(r'^holograms/add/(?P<field_name>\w+)$', 'add_attribute'),    
    url(r'^holograms/remove/(?P<field_name>\w+)$', 'remove_attribute'),    
    url(r'^audiobooks$', 'audiobooks'),
    url(r'^audiobooks/(?P<pk>\d+)$', 'audiobooks'),
    url(r'^audiobooks/add/(?P<field_name>\w+)$', 'add_attribute'),    
    url(r'^audiobooks/remove/(?P<field_name>\w+)$', 'remove_attribute'),    

    url(r'^admin/', include(admin.site.urls)),
)
