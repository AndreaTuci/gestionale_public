from django.urls import path
from . import views
from gestionale_cfp import settings
from django.conf.urls.static import static

# from django.conf.urls import url

urlpatterns = [
    path('', views.index, name="index"),
    path('testbadge/', views.generate_barcodes, name='generate-badges'),
    path('crea-studente/', views.create_student_user, name='create-student-user'),
    path('primo-accesso/crea/', views.first_access_create_view, name="first-access"),
    # url(r'^logout/$', views.logout, name="core-logout"),
]
