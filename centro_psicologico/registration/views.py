from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        #Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder': 'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder': 'Direccion email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder': 'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder': 'Repite la contraseña'})
        return form

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # Recuperar el objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # Recuperar el objeto que se va editar
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form
    
@method_decorator(login_required, name='dispatch')
class ProfileDelete(DeleteView):
    model = Profile
    template_name = 'registration/profile_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = super(ProfileDelete, self).get_object(queryset)
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        user.delete()
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
def eliminar_usuario(request, user):
    profile = Profile.objects.get(user=user)
    profile.delete()

    return redirect('index')
