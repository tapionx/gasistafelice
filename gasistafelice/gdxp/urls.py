from django.conf.urls.defaults import *
try:
    from django.conf.urls import url
except ImportError as e:
    # Using Django < 1.4
    from django.conf.urls.defaults import url

urlpatterns = patterns('',
    (r'^suppliers/$', 'gdxp.views.suppliers'),

    #(r'^supplierstock/(?P<stock_id>[0-9]+)/$', 'rdf_gf.views.show_supplier_stock'),
    #(r'^supplierstock/(?P<stock_id>[0-9]+)/catalog/$', 'rdf_gf.views.show_catalog_from_product'),
)
