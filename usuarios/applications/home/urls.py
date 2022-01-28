from django.urls import path

from . import views

app_name = 'home_app'

urlpatterns = [
    path('', view=views.HomePage.as_view(), name='home'),
    path('prueba/', view=views.TemplatePruebaMixin.as_view(), name='prueba-mixin')
]
