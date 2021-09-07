from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('copartes/', views.copartes),
    path('coparte/<int:coparte_id>', views.coparte),
    path('countcopartepais/<str:pais>', views.countcopartepais),
    #path('countpropcoparte/', views.countpropcoparte),
    path('countpropuesta/<str:id>', views.countpropuesta),
    path('countinformeintermedio/<str:id>', views.countinformeintermedio),
    path('countinformefinal/<str:id>', views.countinformefinal),
    path('countic/', views.countic),
    path('countpropic/<str:id>', views.countpropic),
    path('countinfic/<str:id>', views.countinfic),
    path('countae/', views.countae),
]