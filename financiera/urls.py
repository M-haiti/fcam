from django.urls import path
from . import views

urlpatterns = [
    path('countdesembolsos/<int:ano>', views.countdesembolsos),
    path('countingresos/<int:donante_fuente>', views.countingresos),
    path('displaydesembolsosprop/<int:propuesta>', views.displaydesembolsosprop),
    path('displaydesembolsosae/<int:apoyoestrategico>', views.displaydesembolsosae),
     path('displaydesembolsosic/<int:iniciativaconjunta>', views.displaydesembolsosic),
    path('displayingreso/<int:id>', views.displayingreso)
]