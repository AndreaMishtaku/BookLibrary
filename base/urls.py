from django.urls import path
from base import views

urlpatterns=[
    path('',views.kryefaqja,name="kryefaqja"),
    path('logout',views.dil,name='dil'),
    path('book/<pk>/',views.liber,name='liber'),
    path('kontakt',views.kontakt,name='kontakt'),
    path('profili',views.profili,name='profili'),
    path('librat',views.librat,name='librat'),
    path('search',views.search,name='kerkimi'),
    path('rekomandimet',views.rekomandimet,name='rekomandimet'),
]