from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate, ProfileDelete, eliminar_usuario

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('profile/email/', EmailUpdate.as_view(), name='profile_email'),
    path('profile/delete/<int:pk>/', ProfileDelete.as_view(), name='profile_delete'),
    path('eliminacionUsuario/<int:id>', eliminar_usuario)
]
