from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from .forms import ReservationForm
from .models import ReservaHora
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.

class InicioPaginaView(TemplateView):
    template_name = "core/index.html"

class TerapiasView(TemplateView):
    template_name = "core/terapias.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        reservaform = ReservationForm(request.POST)
        if reservaform.is_valid():
            reserva = reservaform.save()  # Guardar la reserva y obtener el objeto
            return redirect('pagos', reserva_id=reserva.id)  # Redirigir a la vista de pagos con el ID de la reserva
        return self.render_to_response(self.get_context_data(form=reservaform))

class QuienesSomosView(TemplateView):
    template_name = "core/quienes-somos.html"

class CarritoView(TemplateView):
    template_name = "core/carrito.html"

class PagosView(TemplateView):
    template_name = "core/pagos.html"

    
    
def listar_reserva(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            reservas = ReservaHora.objects.all()
        else:
            reservas = ReservaHora.objects.filter(user=request.user)
        
        page = request.GET.get('page', 1)
        
        try:
            paginator = Paginator(reservas, 5)
            reservas = paginator.get_page(page)
        except:
            raise Http404
        
        data = {
            'reservas': reservas,
            'paginator': paginator
        }
        return render(request, 'core/reserva/listar.html', data)
    else:
        return redirect('login')  # Redirige a login si no está autenticado

def modificar_reserva(request, id):
    
    reservas = get_object_or_404(ReservaHora, id=id)
    
    if request.method == 'POST':
        formulario = ReservationForm(data=request.POST, instance=reservas)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_reserva')
    else:
        formulario = ReservationForm(instance=reservas)
        
    data = {
        'form': ReservationForm(instance=reservas)
    }
    
    return render(request, 'core/reserva/modificar.html',data)

def eliminar_reserva(request, id):
    reserva = get_object_or_404(ReservaHora, id=id)
    reserva.delete()

    return redirect('listar_reserva')  


class RedirectView(TemplateView):
    template_name = "core/redirect.html"

class RedirectConfirmarView(TemplateView):
    template_name = "core/redirect_confirmar.html"

@csrf_exempt
def guardar_reservas(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            for reserva_data in data:
                # Verificar si ya existe una reserva con la misma fecha y hora
                existing_reserva = ReservaHora.objects.filter(
                    user=request.user,
                    fecha=reserva_data['fecha'],
                    hora=reserva_data['hora']
                ).first()
                
                if not existing_reserva:
                    reserva = ReservaHora(
                        user=request.user,
                        nombre=reserva_data['nombre'],
                        apellido=reserva_data['apellido'],
                        telefono=reserva_data['telefono'],
                        tipo_consulta=reserva_data['tipo'],
                        tipo_modalidad=reserva_data['tipo2'],
                        fecha=reserva_data['fecha'],
                        hora=reserva_data['hora']
                    )
                    reserva.save()
            return HttpResponse(status=200)
        except json.JSONDecodeError as e:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)