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
	url(r'^admin$', 'main.views.admin'),
	url(r'^api/', include(v1_api.urls)),
	url(r'^griferos', 'main.views.griferos'),
	url(r'^tanque/estado', 'main.views.tanques'),
	url(r'^ventas/update/$', 'main.views.update_ventas'),
	url(r'^ventas/combustible', 'main.views.consumo_combustibles'),
	url(r'^ventas/(\d{4})/(\d{1,2})/(\d{1,2})/$', 'main.views.ventas_dia'),
	url(r'^ventas/(\d{4})/(\d{1,2})/$', 'main.views.ventas_mes'),
	url(r'^ventas/(\d{4})/$', 'main.views.ventas_anio'),
	url(r'^ventas/departamento/([a-zA-Z]+)/$', 'main.views.ventas_departamento'),
	url(r'^ventas/estacion/$', 'main.views.ventas_estacion'),
	url(r'^json/ventas/estacion/$', 'main.views.jsonVentas'),
)