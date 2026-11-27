from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import ejemplo, empleado, Vehiculo, Formulario
from .forms import crearForms
from decimal import Decimal
from django.db import transaction
from django.contrib import messages
import re
from .models import Carrito, CarritoItem, Pedido, PedidoItem

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def apply(request):
    return HttpResponse("Bienvenido a mi Sitio Web.. :)")

def pagina(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def inicio(request):
    return render(request, 'index.html')

def marcas(request):
    lista_vehiculos = Vehiculo.objects.all()

    marcas = (
        Vehiculo.objects
        .values_list('marca', flat=True)
        .distinct()
        .order_by('marca')
    )

    return render(request, 'marcas.html', {
        'marcas': marcas,
        'vehiculos': lista_vehiculos
    })

def vehiculos(request):
    lista_vehiculos = Vehiculo.objects.filter(
        activo=True
    ).select_related('categoria')

    return render(request, 'vehiculos.html', {
        'vehiculos': lista_vehiculos
    })

def galeria(request):
    lista_vehiculos = Vehiculo.objects.all()
    return render(request, 'galeria.html', {
        'vehiculos': lista_vehiculos
    })


def ofertas(request):
    lista_vehiculos = Vehiculo.objects.filter(
        en_oferta=True,
        activo=True,
        stock__gt=0
    )

    return render(request, 'ofertas.html', {
        'vehiculos': lista_vehiculos
    })

def contacto(request):
    return render(request, 'contacto.html')

def login(request):
    error = ''

    if request.method == 'POST':
        print("LOGIN RECIBIDO:", request.method)
        username = request.POST.get('usuario', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            auth_login(request, usuario)
            return redirect('inicio')
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'login.html', {
        'error': error
    })


def registro(request):
    errores = []

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            errores.append('Todos los campos son obligatorios.')

        if password1 != password2:
            errores.append('Las contraseñas no coinciden.')

        if User.objects.filter(username=username).exists():
            errores.append('Ese nombre de usuario ya está registrado.')

        if User.objects.filter(email=email).exists():
            errores.append('Ese correo ya está registrado.')

        if password1 and password1 == password2:
            try:
                validate_password(password1)
            except ValidationError as error:
                errores.extend(error.messages)

        if not errores:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            from django.contrib import messages
            messages.success(
                request, '¡Tu cuenta se creó correctamente! Ya puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'registro.html', {
        'errores': errores
    })

@user_passes_test(lambda usuario: usuario.is_superuser)
def gestionar_usuarios(request):
    usuarios = User.objects.all().order_by('id')
    return render(request, 'gestionar_usuarios.html', {
        'usuarios': usuarios
    })

@user_passes_test(lambda usuario: usuario.is_superuser)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if username and email:
            if User.objects.filter(username=username).exclude(id=usuario.id).exists():
                return render(request, 'editar_usuario.html', {
                    'usuario': usuario,
                    'error': 'Ese nombre de usuario ya está registrado.'
                })

            if User.objects.filter(email=email).exclude(id=usuario.id).exists():
                return render(request, 'editar_usuario.html', {
                    'usuario': usuario,
                    'error': 'Ese correo ya está registrado.'
                })

            usuario.username = username
            usuario.email = email
            usuario.save()

            return redirect('gestionar_usuarios')

        return render(request, 'editar_usuario.html', {
            'usuario': usuario,
            'error': 'Completa todos los campos.'
        })

    return render(request, 'editar_usuario.html', {
        'usuario': usuario
    })


@user_passes_test(lambda usuario: usuario.is_superuser)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if usuario.is_superuser:
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        return redirect('gestionar_usuarios')

    return render(request, 'eliminar_usuario.html', {
        'usuario': usuario
    })


@login_required(login_url='login')
def perfil(request):
    usuario = request.user

    return render(request, 'perfil.html', {
        'usuario': usuario
    })

@login_required(login_url='login')
def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        return redirect('inicio')

    return redirect('perfil')


def api_vehiculos(request):
    vehiculos = Vehiculo.objects.select_related('categoria').all()

    datos = []
    for vehiculo in vehiculos:
        datos.append({
            'id': vehiculo.id,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'anio': vehiculo.anio,
            'precio': str(vehiculo.precio),
            'descripcion': vehiculo.descripcion,
            'categoria': vehiculo.categoria.nombre,
            'imagen': vehiculo.imagen,
            'en_oferta': vehiculo.en_oferta,
            'audio_motor': vehiculo.audio_motor,
            'stock': vehiculo.stock,
            'precio_anterior': (
                str(vehiculo.precio_anterior)
                if vehiculo.precio_anterior is not None
                else None
            ),
        })

    return JsonResponse({'vehiculos': datos})

def formulario(request):

    if request.method == 'POST':
        form = crearForms(request.POST)

        if form.is_valid():

            Formulario.objects.create(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion']
            )

            return render(request, 'formulario.html', {
                'form': crearForms(),
                'mensaje': '¡Formulario guardado correctamente!'
            })

    else:
        form = crearForms()

    return render(request, 'formulario.html', {
        'form': form
    })

@login_required(login_url='login')
def carrito(request):

    carrito_usuario, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    productos = carrito_usuario.productos.select_related(
        'vehiculo',
        'vehiculo__categoria'
    )

    total = sum(
        (item.subtotal for item in productos),
        Decimal('0.00')
    )

    return render(request, 'carrito.html', {
    'carrito': carrito_usuario,
    'items': productos,
    'total': total
    })

@login_required(login_url='login')
def agregar_carrito(request, id):

    if request.method != 'POST':
        return redirect('vehiculos')

    vehiculo = get_object_or_404(
        Vehiculo,
        id=id,
        activo=True
    )

    if vehiculo.stock < 1:
        messages.error(request, 'Este vehículo no está disponible.')
        return redirect('vehiculos')

    carrito_usuario, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    item, creado = CarritoItem.objects.get_or_create(
        carrito=carrito_usuario,
        vehiculo=vehiculo
    )

    if not creado:
        if item.cantidad >= vehiculo.stock:
            messages.error(
                request,
                'No hay más unidades disponibles de este vehículo.'
            )
            return redirect('carrito')

        item.cantidad += 1
        item.save()

    messages.success(
        request,
        f'{vehiculo.marca} {vehiculo.modelo} agregado al carrito.'
    )

    return redirect('carrito')

@login_required(login_url='login')
def eliminar_carrito(request, id):

    if request.method == 'POST':
        carrito_usuario, creado = Carrito.objects.get_or_create(
            usuario=request.user
        )

        item = get_object_or_404(
            CarritoItem,
            id=id,
            carrito=carrito_usuario
        )

        item.delete()

        messages.success(request, 'Vehículo eliminado del carrito.')

    return redirect('carrito')


@login_required(login_url='login')
def finalizar_compra(request):

    carrito_usuario, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    productos = list(
        carrito_usuario.productos.select_related('vehiculo')
    )

    total = sum(
        (item.subtotal for item in productos),
        Decimal('0.00')
    )

    if not productos:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    if request.method == 'GET':
        return render(request, 'pago.html', {
            'productos': productos,
            'total': total
        })

    titular = request.POST.get('titular', '').strip()
    tarjeta = request.POST.get('numero_tarjeta', '').strip()
    vencimiento = request.POST.get('vencimiento', '').strip()
    cvv = request.POST.get('cvv', '').strip()

    errores = []

    if not titular:
        errores.append('Escribe el nombre del titular ficticio.')

    if not re.fullmatch(r'\d{16}', tarjeta):
        errores.append(
            'El número debe contener exactamente 16 dígitos.'
        )

    if not re.fullmatch(r'(0[1-9]|1[0-2])/\d{2}', vencimiento):
        errores.append(
            'El vencimiento debe tener el formato MM/AA.'
        )

    if not re.fullmatch(r'\d{3}', cvv):
        errores.append(
            'El CVV debe contener exactamente 3 dígitos.'
        )

    if errores:
        return render(request, 'pago.html', {
            'productos': productos,
            'total': total,
            'errores': errores
        })

    try:
        with transaction.atomic():

            carrito_usuario = Carrito.objects.select_for_update().get(
                usuario=request.user
            )

            productos = list(
                carrito_usuario.productos.select_related('vehiculo')
            )

            if not productos:
                messages.error(request, 'Tu carrito está vacío.')
                return redirect('carrito')

            total = Decimal('0.00')
            vehiculos_actualizados = []

            for item in productos:

                vehiculo = Vehiculo.objects.select_for_update().get(
                    id=item.vehiculo_id
                )

                if (
                    not vehiculo.activo
                    or item.cantidad < 1
                    or item.cantidad > vehiculo.stock
                ):
                    messages.error(
                        request,
                        f'No hay disponibilidad para '
                        f'{vehiculo.marca} {vehiculo.modelo}.'
                    )
                    return redirect('carrito')

                total += vehiculo.precio * item.cantidad

                vehiculos_actualizados.append(
                    (vehiculo, item.cantidad)
                )

            pedido = Pedido.objects.create(
                usuario=request.user,
                total=total,
                estado='confirmado',
                estado_pago='prueba_aprobada'
            )

            for item in productos:

                vehiculo = next(
                    v for v, cantidad in vehiculos_actualizados
                    if v.id == item.vehiculo_id
                )

                PedidoItem.objects.create(
                    pedido=pedido,
                    vehiculo=vehiculo,
                    cantidad=item.cantidad,
                    precio_unitario=vehiculo.precio
                )

            for vehiculo, cantidad in vehiculos_actualizados:

                vehiculo.stock -= cantidad

                if vehiculo.stock == 0:
                    vehiculo.activo = False

                vehiculo.save()

            carrito_usuario.productos.all().delete()

        messages.success(
            request,
            '¡Pago simulado aprobado! Tu compra se registró correctamente.'
        )

        return redirect('pedido_confirmado', id=pedido.id)

    except (Carrito.DoesNotExist, Vehiculo.DoesNotExist):
        messages.error(
            request,
            'No se pudo completar la compra. Actualiza tu carrito.'
        )
        return redirect('carrito')

@login_required(login_url='login')
def pedido_confirmado(request, id):

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('productos__vehiculo'),
        id=id,
        usuario=request.user
    )

    return render(request, 'pedido_confirmado.html', {
        'pedido': pedido
    })

@login_required(login_url='login')
def recibo_pedido(request, id):

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('productos__vehiculo'),
        id=id,
        usuario=request.user,
        estado_pago='prueba_aprobada'
    )

    return render(request, 'recibo.html', {
        'pedido': pedido
    })

@login_required(login_url='login')
def mis_pedidos(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-fecha_pedido')

    return render(request, 'mis_pedidos.html', {
        'pedidos': pedidos
    })