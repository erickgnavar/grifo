from django.db import models

DEPARTAMENTOS = (
    ('AMAZONAS', 'AMAZONAS'),
    ('ANCASH', 'ANCASH'),
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
    nombre = models.CharField(max_length=20, unique=True)
    precio = models.FloatField(null=False)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
    fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

    def __unicode__(self):
        return self.nombre


class EstacionServicio(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    direccion = models.CharField(max_length=40)
    departamento = models.CharField(max_length=30, choices=DEPARTAMENTOS, null=False)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
    fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

    def __unicode__(self):
        return '%s - %s' % (self.departamento, self.direccion)


class Grifero(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    usuario = models.CharField(max_length=20, unique=True)
    clave = models.CharField(max_length=20, null=False)
    estado = models.CharField(max_length=20, choices=GRIFERO_ESTADOS, null=False)
    estacion = models.ForeignKey(EstacionServicio, blank=True)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
    fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

    def __unicode__(self):
        return self.nombre


class Modulo(models.Model):
    numero = models.IntegerField(null=False)
    combustibles = models.ManyToManyField(Combustible)
    estacion = models.ForeignKey(EstacionServicio, null=False)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
    fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

    def __unicode__(self):
        return str(self.numero)


class Venta(models.Model):
    cantidad = models.IntegerField(null=False)
    estacion = models.ForeignKey(EstacionServicio, null=False)
    combustible = models.ForeignKey(Combustible, null=False)
    documento_cliente = models.IntegerField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=20, null=True, blank=True)
    grifero = models.ForeignKey(Grifero, null=False)
    subtotal = models.FloatField(null=False, blank=True, default=0)
    total = models.FloatField(null=False, blank=True, default=0)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)

    # def save(self, *args, **kwargs):
    #   try:
    #       tanque = Tanque.objects.get(combustible__nombre=self.combustible.nombre, estacion__nombre=self.estacion.nombre)
    #       if tanque:
    #           if self.cantidad <= tanque.contenido:
    #               tanque.contenido -= self.cantidad
    #               tanque.save()
    #               super(Venta, self).save(*args, **kwargs)
    #           else:
    #               raise ValidationError('Combustible no disponible en tanque')
    #   except:
    #       raise ValidationError('Tanque Inexistente')

    def __unicode__(self):
        return "%i %s :  %f" % (self.cantidad, self.combustible, self.cantidad * self.combustible.precio)


class Tanque(models.Model):
    combustible = models.ForeignKey(Combustible, null=True)
    capacidad = models.FloatField()
    contenido = models.FloatField()
    estacion = models.ForeignKey(EstacionServicio, null=True)
    fecha_creado = models.DateTimeField('fecha de creacion', auto_now_add=True)
    fecha_actualizado = models.DateTimeField('fecha de actualizacion', auto_now=True)

    def __unicode__(self):
        return str(self.combustible.nombre)
