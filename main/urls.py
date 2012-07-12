from django.conf.urls import patterns, include, url

from tastypie.api import Api
from api.resources import *

v1_api = Api(api_name='v1')
v1_api.register(GriferoResource())
v1_api.register(CombustibleResource())
v1_api.register(EstacionServicioResource())
v1_api.register(ModuloResource())
v1_api.register(TanqueResource())
v1_api.register(VentaResource())

urlpatterns = patterns('',
    url(r'^$', 'main.views.home'),
    url(r'^login/$', 'main.views.ingresar'),
    url(r'^logout/$', 'main.views.salir'),
    url(r'^reportes/$', 'main.views.reportes'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^combustible/consumo', 'main.views.combustible_consumo'),
    url(r'^combustible/precios/$', 'main.views.combustible_precios'),
    url(r'^combustible/precio/actualizar/(\d{1,2}\.\d{1,2}?)/(\d{1})/$', 'main.views.combustible_precio_actualizar'),
    url(r'^json/venta/estacion/$', 'main.views.json_venta_estacion'),
    url(r'^tanque/estado/$', 'main.views.tanque_estado'),
    url(r'^venta/(\d{4})/$', 'main.views.venta_fecha_anio'),
    url(r'^venta/combustible/(\d{1,2})/$', 'main.views.venta_combustible'),
    url(r'^venta/(\d{4})/(\d{1,2})/$', 'main.views.venta_fecha_mes'),
    url(r'^venta/(\d{4})/(\d{1,2})/(\d{1,2})/$', 'main.views.venta_fecha_dia'),
    url(r'^venta/departamento/([a-zA-Z]+)/$', 'main.views.venta_departamento'),
    url(r'^venta/estacion/$', 'main.views.venta_estacion'),
    url(r'^grifero/listado/$', 'main.views.grifero_listado'),
)
