from django.urls import path
from . import views
from .views import InicioPaginaView, TerapiasView, QuienesSomosView, CarritoView, PagosView, RedirectConfirmarView, listar_reserva, modificar_reserva, eliminar_reserva, RedirectView

urlpatterns = [
    path('', InicioPaginaView.as_view(), name="index"),
    path('terapias', TerapiasView.as_view(), name="terapias"),
    path('quienes-somos/', QuienesSomosView.as_view(), name="quienes-somos"),
    path('carrito', CarritoView.as_view(), name="carrito"),
    path('pagos', PagosView.as_view(), name="pagos"),
    path('redirect/', RedirectView.as_view(), name='wait_and_redirect'),
    path('redirect_confirmar/', RedirectConfirmarView.as_view(), name='confirmar'),
    path('guardar-reservas/', views.guardar_reservas, name='guardar_reservas'),
    path('listar-reservas/', listar_reserva, name="listar_reserva"),
    path('modificar-reservas/<id>/', modificar_reserva, name="modificar_reserva"),
    path('eliminar-reservas/<id>/', eliminar_reserva, name="eliminar_reserva"),
    
]
