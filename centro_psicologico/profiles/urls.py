from django.urls import path
from .views import ProfileListView, ProfileDetailView, ProfileDelete

profiles_patterns = ([
    path('', ProfileListView.as_view(), name='list'),
    path('<username>/', ProfileDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', ProfileDelete.as_view(), name='delete'),
], "profiles")
