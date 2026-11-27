from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.apply, name="apply"),
    path("miPagina/", views.pagina, name="miPagina"),
    path("index/", views.index, name="index"),
    path("", views.inicio, name="inicio"),

    path("marcas/", views.marcas, name="marcas"),
    path("vehiculos/", views.vehiculos, name="vehiculos"),
    path('api/vehiculos/', views.api_vehiculos, name='api_vehiculos'),
    path("galeria/", views.galeria, name="galeria"),
    path("ofertas/", views.ofertas, name="ofertas"),
    path("contacto/", views.contacto, name="contacto"),

    path("login/", views.login, name="login"),
    path("perfil/", views.perfil, name="perfil"),
    path("registro/", views.registro, name="registro"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),

    path("gestionar-usuarios/", views.gestionar_usuarios, name="gestionar_usuarios"),
    path("editar-usuario/<int:id>/", views.editar_usuario, name="editar_usuario"),
    path("eliminar-usuario/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),

    path("formulario/", views.formulario, name="formulario"),

    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/eliminar/<int:id>/", views.eliminar_carrito, name="eliminar_carrito"),
    
    path("finalizar-compra/", views.finalizar_compra, name="finalizar_compra"),
    path("pedido-confirmado/<int:id>/", views.pedido_confirmado, name="pedido_confirmado"),
    path("recibo/<int:id>/", views.recibo_pedido, name="recibo_pedido"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
]
