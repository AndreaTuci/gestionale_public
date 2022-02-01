from django.urls import path
from . import views

urlpatterns = [
    path('contratti/docenti/', views.display_teacher_agreement, name="teacher-agreement-list"),
    path('contratti/docenti/crea/', views.TeacherAgreementCreateView.as_view(), name="teacher-agreement-create"),
    path('contratti/docenti/<int:pk>/', views.teacher_agreement_detail_view, name="teacher-agreement-detail"),
    path('contratti/docenti/modifica/<int:pk>/', views.TeacherAgreementUpdateView.as_view(), name="teacher-agreement-update"),
    path('contratti/docenti/cancella/<int:pk>/', views.delete_teacher_agreement, name="teacher-agreement-delete"),

    path('magazzino/materiali/', views.WarehouseListView.as_view(), name="warehouse-list"),
    path('magazzino/movements/add', views.warehouse_scan_code, name="warehouse-code"),
    path('magazzino/test', views.test_htmx, name='test-htmx'),
    path('magazzino/movements/create/<slug:barcode>/', views.warehouse_movement_create, name='warehouse-movement-create'),
    path('magazzino/movements/add/<slug:barcode>/', views.movement_add, name='warehouse-movement-add'),

    path('timecard/tutor/detail/pk=<int:pk>month=<int:month>year=<int:year>/', views.timecard_entry_detail, name='timecard-detail'),
    path('timecard/tutor/detail/update/<int:pk>/', views.timecard_entry_update, name='timecard-update'),
    path('timecard/tutor/list/<int:pk>/', views.timecard_list, name='timecard-list'),
    path('timecard/download/pk=<int:pk>month=<int:month>year=<int:year>/', views.download_timecard, name='timecard-download'),
    path('timecard/download/all/month=<int:month>year=<int:year>/', views.download_all_timecards, name='timecard-download-all'),

]
