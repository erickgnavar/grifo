from django.db import models

DEPARTAMENTOS = (
	('AMAZONAS', 'AMAZONAS'),
	('ANCASH', 'ANCASH') ,
	('APURIMAC', 'APURIMAC'),
	('AREQUIPA', 'AREQUIPA'),
	('AYACUCHO', 'AYACUCHO'),
	('CAJAMARCA', 'CAJAMARCA'),
	('CALLAO', 'CALLAO'),
	('CUSCO', 'CUSCO'),
	('HUANCAVELICA', 'HUANCAVELICA'),
	('HUANUCO', 'HUANUCO'),
	('ICA', 'ICA'),
	('JUNIN', 'JUNIN'),
	('LALIBERTAD', 'LA LIBERTAD'),
	('LAMBAYEQUE', 'LAMBAYEQUE'),
	('LIMA', 'LIMA'),
	('LORETO', 'LORETO'),
	('MADREDEDIOS', 'MADRE DE DIOS'),
	('MOQUEGUA', 'MOQUEGUA'),
	('PASCO', 'PASCO'),
	('PIURA', 'PIURA'),
	('PUNO', 'PUNO'),
	('SANMARTIN', 'SAN MARTIN'),
	('TACNA', 'TACNA'),
	('TUMBES', 'TUMBES'),
	('UCAYALI', 'UCAYALI'),
)

GRIFERO_ESTADOS = (
	('turno', 'En turno'),
	('descanso', 'En descanso'),
)

class Combustible(models.Model):
	tipo = models.CharField(max_length=20)
	precio = models.FloatField()
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
	fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

	def __unicode__(self):
		return self.tipo


class EstacionServicio(models.Model):
	nombre = models.CharField(max_length=20)
	direccion = models.CharField(max_length=40)
	departamento = models.CharField(max_length=30, choices=DEPARTAMENTOS)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
	fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

	def __unicode__(self):
		return self.nombre


class Grifero(models.Model):
	nombre = models.CharField(max_length=30)
	usuario = models.CharField(max_length=20, unique=True)
	clave = models.CharField(max_length=20, null=False)
	estado = models.CharField(max_length=20, choices=GRIFERO_ESTADOS)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
	fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

	def __unicode__(self):
		return self.nombre


class Modulo(models.Model):
	numero = models.IntegerField()
	combustibles = models.ManyToManyField(Combustible)
	estacion = models.ForeignKey(EstacionServicio)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
	fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

	def __unicode__(self):
		return str(self.numero)


class Venta(models.Model):
	cantidad = models.IntegerField()
	estacion = models.ForeignKey(EstacionServicio)
	combustible = models.ForeignKey(Combustible, null=False)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)

	def __unicode__(self):
		return "%i - %s" % (self.cantidad, self.combustible) 


class Recibo(models.Model):
	items = models.ManyToManyField(Venta)
	grifero = models.ForeignKey(Grifero, null=False)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)


class Tanque(models.Model):
	combustible = models.ForeignKey(Combustible)
	capacidad = models.FloatField()
	contenido = models.FloatField()
	estacion = models.ForeignKey(EstacionServicio)
	fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
	fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

	def __unicode__(self):
		return str(self.combustible.tipo)
