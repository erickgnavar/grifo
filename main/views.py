from datetime import datetime, date
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from models import *

def home(request):
	return HttpResponseRedirect('/main/admin')

def error_500(request):
	return render_to_response('500.html')

def error_404(request):
	return render_to_response('404.html')

def griferos(request):
	griferos = Grifero.objects.all()
	return render_to_response('main/griferos.html', {'griferos': griferos})

def admin(request):
	return render_to_response('main/admin.html')

def consumo_combustibles(request):
	ventas = Venta.objects.all()
	
	data = graficoVentas(ventas)

	data_meses = [
		{'mes': 'enero', 'cantidad': 0},
		{'mes': 'febrero', 'cantidad': 0},
		{'mes': 'marzo', 'cantidad': 0},
		{'mes': 'abril', 'cantidad': 0},
		{'mes': 'mayo', 'cantidad': 0},
		{'mes': 'junio', 'cantidad': 0},
		{'mes': 'julio', 'cantidad': 0},
		{'mes': 'agosto', 'cantidad': 0},
		{'mes': 'septiembre', 'cantidad': 0},
		{'mes': 'octubre', 'cantidad': 0},
		{'mes': 'noviembre', 'cantidad': 0},
		{'mes': 'diciembre', 'cantidad': 0},
	]

	for venta in ventas:
		mes = (int)(venta.fecha_creado.strftime('%m'))
		(data_meses[mes - 1])['cantidad'] += venta.cantidad

	return render_to_response('main/consumo_combustibles.html', {'data': data, 'data_meses': data_meses})

def ventas_dia(request, anio, mes, dia):
	# fecha_pedida = date((int)(anio), (int)(mes), (int)(dia))
	fecha = '%s - %s - %s' % (anio, mes, dia)
	anio = (int)(anio)
	mes = (int)(mes)
	dia = (int)(dia)
	# ventas = Venta.objects.filter(fecha_creado__startswith=fecha_pedida)
	ventas = Venta.objects.filter(fecha_creado__year=anio, fecha_creado__month=mes, fecha_creado__day=dia)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/reporte_ventas.html', {'fecha': fecha, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

def ventas_mes(request, anio, mes):
	fecha = '%s - %s' % (anio, mes)
	anio = (int)(anio)
	mes = (int)(mes)
	ventas = Venta.objects.filter(fecha_creado__year=anio, fecha_creado__month=mes)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/reporte_ventas.html', {'fecha': fecha, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

def ventas_anio(request, anio):
	anio = (int)(anio)
	ventas = Venta.objects.filter(fecha_creado__year=anio)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/reporte_ventas.html', {'fecha': anio, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

def ventas_departamento(request, departamento):
	estaciones = EstacionServicio.objects.filter(departamento=departamento.upper())

	data = []

	for estacion in estaciones:
		data.append({'estacion': estacion.nombre, 'cantidad': 0, 'monto': 0})
	
	ventas = Venta.objects.filter(estacion__departamento=departamento.upper())

	for venta in ventas:
		for item in data:
			if venta.estacion.nombre == item['estacion']:
				item['cantidad'] += venta.cantidad
				item['monto'] += venta.cantidad * venta.combustible.precio

	return render_to_response('main/reporte_ventas_departamento.html', {'ventas': ventas, 'data': data, 'departamento': departamento})


def ventas_estacion(request):
	return render_to_response('main/reporte_ventas_estacion.html')

def jsonVentas(request):
	data = {}
	labels = []
	values = []
	estaciones = EstacionServicio.objects.all()
	combustibles = Combustible.objects.all()
	for combustible in combustibles:
		labels.append(combustible.nombre)
	for estacion in estaciones:
		ventas = Venta.objects.filter(estacion__nombre=estacion.nombre)
		cantidades = []
		for combustible in combustibles:
			can = 0
			for v in ventas.filter(combustible__nombre=combustible.nombre):
				can += v.cantidad
			cantidades.append(can)
		v = {}
		v['label'] = estacion.nombre
		v['values'] = cantidades
		values.append(v)
	data['label'] = labels
	data['values'] = values
	return HttpResponse(json.dumps(data), mimetype="application/json")


def prueba(request, nombre):
	return HttpResponse(nombre)

#Funciones aparte

def graficoVentas(ventas):
	combustibles = Combustible.objects.all()

	data = []

	for combustible in combustibles:
		data.append({'nombre': combustible.nombre, 'cantidad': 0, 'monto': 0})

	for venta in ventas:
		for item in data:
			if venta.combustible.nombre == item['nombre']:
				item['cantidad'] += venta.cantidad
				item['monto'] += venta.combustible.precio * venta.cantidad
	return data

def graficoVentasEstacion(ventas):
	estaciones = EstacionServicio.objects.all()
	data_estaciones = []
	for estacion in estaciones:
		data_estaciones.append({'estacion': estacion.nombre, 'cantidad': 0})

	for venta in ventas:
		for item in data_estaciones:
			if venta.estacion.nombre == item['estacion']:
				item['cantidad'] += venta.cantidad
	return data_estaciones