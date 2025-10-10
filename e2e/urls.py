from django.urls import path
from .views import CallCommandView

urlpatterns = [
    path('call-command/<str:command>', CallCommandView.as_view(), name='call-command'),
]

