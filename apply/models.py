from django.db import models
from django.conf import settings
import uuid

class ejemplo(models.Model):
    edad = models.IntegerField()

    def __str__(self):
        return str(self.edad)

class empleado(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre + ' - ' + str(self.edad)


class alumno(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    carrera = models.CharField(max_length=150)

    def __str__(self):
        return (
            'Nombre: ' + self.nombre
            + ' Apellido: ' + self.apellido
            + ' Edad: ' + str(self.edad)
            + ' Carrera: ' + self.carrera
        )

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT
    )

    imagen = models.CharField(max_length=255, blank=True)
    audio_motor = models.CharField(max_length=255, blank=True)

    en_oferta = models.BooleanField(default=False)
    precio_anterior = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    stock = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class Formulario(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Carrito(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrito'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['carrito', 'vehiculo'],
                name='vehiculo_unico_por_carrito'
            )
        ]

    def __str__(self):
        return f"{self.vehiculo} x {self.cantidad}"

    @property
    def subtotal(self):
        return self.vehiculo.precio * self.cantidad

class Pedido(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'En preparación'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('prueba_aprobada', 'Pago de prueba aprobado'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    numero_pedido = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )

    fecha_pedido = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADOS_PAGO,
        default='pendiente'
    )

    comentarios = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido {self.numero_pedido}"
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField(default=1)

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.vehiculo} - Pedido {self.pedido.numero_pedido}"

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad