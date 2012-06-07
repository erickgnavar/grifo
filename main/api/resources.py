from tastypie.resources import ModelResource
from main.models import *

class GriferoResource(ModelResource):
	class Meta:
		queryset = Grifero.objects.all()
		allowed_methods = ['get']
		resource_name = 'grifero'


class CombustibleResource(ModelResource):
	class Meta:
		queryset = Combustible.objects.all()
		allowed_methods = ['get']
		resource_name = 'combustible'


class EstacionServicioResource(ModelResource):
	class Meta:
		queryset = EstacionServicio.objects.all()
		allowed_methods = ['get']
		resource_name = 'estacion_de_servicio'


class ModuloResource(ModelResource):
	class Meta:
		queryset = Modulo.objects.all()
		allowed_methods = ['get']
		resource_name = 'modulo'

class TanqueResource(ModelResource):
	class Meta:
		queryset = Tanque.objects.all()
		allowed_methods = ['get']
		resource_name = 'tanque'


class VentaResource(ModelResource):
	class Meta:
		queryset = Venta.objects.all()
		allowed_methods = ['get']
		resource_name = 'venta'