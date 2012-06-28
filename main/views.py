from datetime import datetime, date
import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *

def home(request):
	return render_to_response('main/home.html', RequestContext(request))

def error_500(request):
	return render_to_response('500.html')

def error_404(request):
	return render_to_response('404.html')

@login_required(login_url='/g/login')
def reportes(request):
	combustibles = Combustible.objects.all()
	return render_to_response('main/reportes.html', {'combustibles': combustibles})

@login_required(login_url='/g/login')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')

def ingresar(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				login(request, acceso)
				return HttpResponseRedirect('/g/')
			else:
				return render_to_response('main/ingresar.html', {'formulario': formulario, 'error': 'Usuario o clave invalidos'}, RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('main/ingresar.html', {'formulario': formulario}, RequestContext(request))

@login_required(login_url='/g/login')
def grifero_listado(request):
	griferos = Grifero.objects.all()
	estaciones = EstacionServicio.objects.all()
	return render_to_response('main/grifero_listado.html', {'griferos': griferos, 'estaciones': estaciones})

@login_required(login_url='/g/login')
def combustible_consumo(request):
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

	return render_to_response('main/combustible_consumo.html', {'data': data, 'data_meses': data_meses})

def tanque_estado(request):
	tanques = Tanque.objects.all()
	return render_to_response('main/tanque_estado.html', {'tanques': tanques})

@login_required(login_url='/g/login')
def combustible_precios(request):
	combustibles = Combustible.objects.all()
	return render_to_response('main/combustible_precios.html', {'combustibles': combustibles})

@login_required(login_url='/g/login')
def combustible_precio_actualizar(request, precio, combustible_id):
	try:
		combustible = Combustible.objects.get(pk=combustible_id)
		if precio > 0:
			combustible.precio = precio
			combustible.save()
			return HttpResponse('OK')
		else:
			return HttpResponse('NOT OK')
	except:
		return HttpResponse('NOT OK')

@login_required(login_url='/g/login')
def venta_combustible(request, id):
	ventas = Venta.objects.filter(combustible__id=id)
	data = graficoVentasEstacion(ventas);
	combustible = Combustible.objects.get(pk=id)
	return render_to_response('main/venta_combustible.html', {'ventas': ventas, 'data': data, 'combustible': combustible})

@login_required(login_url='/g/login')
def venta_fecha_dia(request, anio, mes, dia):
	fecha = '%s - %s - %s' % (anio, mes, dia)
	anio = (int)(anio)
	mes = (int)(mes)
	dia = (int)(dia)
	# ventas = Venta.objects.filter(fecha_creado__startswith=fecha_pedida)
	ventas = Venta.objects.filter(fecha_creado__year=anio, fecha_creado__month=mes, fecha_creado__day=dia)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/venta_fecha.html', {'fecha': fecha, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

@login_required(login_url='/g/login')
def venta_fecha_mes(request, anio, mes):
	fecha = '%s - %s' % (anio, mes)
	anio = (int)(anio)
	mes = (int)(mes)
	ventas = Venta.objects.filter(fecha_creado__year=anio, fecha_creado__month=mes)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/venta_fecha.html', {'fecha': fecha, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

@login_required(login_url='/g/login')
def venta_fecha_anio(request, anio):
	anio = (int)(anio)
	ventas = Venta.objects.filter(fecha_creado__year=anio)
	data = graficoVentas(ventas)
	data_estaciones = graficoVentasEstacion(ventas)
	return render_to_response('main/venta_fecha.html', {'fecha': anio, 'ventas': ventas, 'data': data, 'data_estaciones': data_estaciones})

@login_required(login_url='/g/login')
def venta_departamento(request, departamento):
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

	return render_to_response('main/venta_departamento.html', {'ventas': ventas, 'data': data, 'departamento': departamento})

@login_required(login_url='/g/login')
def venta_estacion(request):
	return render_to_response('main/venta_estacion.html')

def json_venta_estacion(request):
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
				item['monto'] += venta.total
	return data

def graficoVentasEstacion(ventas):
	estaciones = EstacionServicio.objects.all()
	data_estaciones = []
	for estacion in estaciones:
		data_estaciones.append({'estacion': estacion.nombre, 'cantidad': 0, 'monto': 0})

	for venta in ventas:
		for item in data_estaciones:
			if venta.estacion.nombre == item['estacion']:
				item['cantidad'] += venta.cantidad
				item['monto'] += venta.total
	return data_estaciones