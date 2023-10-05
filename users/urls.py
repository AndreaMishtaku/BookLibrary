from django.urls import path
from users import views

urlpatterns=[
    path('',views.identifikohu,name="identifikohu"),
    path('register/',views.regjistrohu,name="regjistrohu"),
]