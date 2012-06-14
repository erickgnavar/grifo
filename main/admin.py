from django.contrib import admin

from models import *

class VentaAdmin(admin.ModelAdmin):
	list_display = ('id', 'cantidad', 'combustible', 'estacion', 'fecha_creado')


class CombustibleAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'precio', 'fecha_creado', 'fecha_actualizado')


class ModuloAdmin(admin.ModelAdmin):
	list_display = ('id', 'numero', 'estacion', 'fecha_creado')


class EstacionServicioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'direccion', 'departamento', 'fecha_creado')


class GriferoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'usuario', 'estado', 'fecha_creado')


class ReciboAdmin(admin.ModelAdmin):
	list_display = ('id', 'grifero', 'documento', 'fecha_creado')

class TanqueAdmin(admin.ModelAdmin):
	list_display = ('id', 'combustible', 'capacidad', 'contenido', 'estacion', 'fecha_actualizado')


admin.site.register(Venta, VentaAdmin)
admin.site.register(Modulo, ModuloAdmin)
admin.site.register(EstacionServicio, EstacionServicioAdmin)
admin.site.register(Grifero, GriferoAdmin)
admin.site.register(Combustible, CombustibleAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Tanque, TanqueAdmin)