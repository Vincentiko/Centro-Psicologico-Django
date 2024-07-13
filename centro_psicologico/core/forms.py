from django import forms
from .models import ReservaHora

class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservaHora
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'tipo_consulta': 'Tipo de Terapia',
            'tipo_modalidad': 'Modalidad',
            'fecha': 'Fecha deseada',
            'hora': 'Seleccione una hora'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'max': '2024-12-31'}),
            'hora': forms.Select(choices=[
                ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'),
                ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'),
                ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00')
            ], attrs={'class': 'form-control'}),
        }