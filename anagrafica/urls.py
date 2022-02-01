from django.urls import path
from . import views
from accounts.views import user_profile_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('classi/', views.ClassroomListView.as_view(), name="classroom-list"),
    path('classi/crea/', views.ClassroomCreateView.as_view(), name="classroom-create"),
    path('classi/<int:pk>/', views.classroom_detail_view, name="classroom-detail"),
    path('classi/modifica/<int:pk>/', views.ClassroomUpdateView.as_view(), name="classroom-update"),
    path('classi/cancella/<int:pk>/', views.ClassroomDeleteView.as_view(), name="classroom-delete"),

    path('convenzioni/', views.ConventionListView.as_view(), name="convention-list"),
    path('convenzioni/crea/', views.ConventionCreateView.as_view(), name="convention-create"),
    path('convenzioni/<int:pk>/', views.convention_detail_view, name="convention-detail"),
    path('convenzioni/modifica/<int:pk>/', views.ConventionUpdateView.as_view(), name="convention-update"),
    path('convenzioni/cancella/<int:pk>/', views.ConventionDeleteView.as_view(), name="convention-delete"),

    path('ditte/', views.CompanyListView.as_view(), name="company-list"),
    path('ditte/aggiunta/', views.companies_add, name="companies-add"),
    path('ditte/crea/', views.CompanyCreateView.as_view(), name="company-create"),
    path('ditte/<int:pk>/', views.company_detail_view, name="company-detail"),
    path('ditte/modifica/<int:pk>/', views.CompanyUpdateView.as_view(), name="company-update"),
    path('ditte/cancella/<int:pk>/', views.CompanyDeleteView.as_view(), name="company-delete"),

    path('comunicazioni/crea/<int:course>/', views.communication_create_course, name="communication-course-create"),
    path('comunicazioni/<int:course>/<int:pk>/', views.communication_course_detail, name="communication-course-detail"),
    path('comunicazioni/studente=<int:student>/', views.communication_student_list, name="communication-student-list"),
    path('comunicazioni/detail/<int:pk>/', views.single_communication_detail, name="single-communication-detail"),
    path('comunicazioni/studente/crea/<int:student>/', views.single_communication_create, name="single-communication-create"),

    path('corsi/', views.CourseListView.as_view(), name="course-list"),
    path('corsi/crea/', views.CourseCreateView.as_view(), name="course-create"),
    path('corsi/<int:pk>/', views.course_detail_view, name="course-detail"),
    path('corsi/inail/<int:pk>/', views.course_detail_inail_view, name="course-detail-inail"),
    path('corsi/modifica/<int:pk>/', views.CourseUpdateView.as_view(), name="course-update"),
    path('corsi/cancella/<int:pk>/', views.CourseDeleteView.as_view(), name="course-delete"),

    path('tipologie-corso/', views.CourseTypeListView.as_view(), name="coursetype-list"),
    path('tipologie-corso/crea/', views.CourseTypeCreateView.as_view(), name="coursetype-create"),
    path('tipologie-corso/<int:pk>/', views.course_type_detail_view, name="coursetype-detail"),
    path('tipologie-corso/modifica/<int:pk>/', views.CourseTypeUpdateView.as_view(), name="coursetype-update"),
    path('tipologie-corso/cancella/<int:pk>/', views.CourseTypeDeleteView.as_view(), name="coursetype-delete"),

    path('provvedimenti-disciplinari/', views.DisciplinaryMeasureListView.as_view(), name="disciplinarymeasure-list"),
    path('provvedimenti-disciplinari/studente/<int:student>/', views.DisciplinaryMeasureListByStudentView.as_view(), name="disciplinarymeasure-list-by-student"),
    path('provvedimenti-disciplinari/crea/', views.DisciplinaryMeasureCreateView.as_view(),
         name="disciplinarymeasure-create"),
    path('provvedimenti-disciplinari/crea/course=<int:course>', views.DisciplinaryMeasureCourseCreateView.as_view(),
         name="disciplinarymeasure-course-create"),
    path('provvedimenti-disciplinari/<int:pk>/', views.disciplinary_measure_detail_view,
         name="disciplinarymeasure-detail"),
    path('provvedimenti-disciplinari/modifica/<int:pk>/', views.DisciplinaryMeasureUpdateView.as_view(),
         name="disciplinarymeasure-update"),
    path('provvedimenti-disciplinari/cancella/<int:pk>/', views.DisciplinaryMeasureDeleteView.as_view(),
         name="disciplinarymeasure-delete"),

    path('settori/', views.SectorListView.as_view(), name="sector-list"),
    path('settori/crea/', views.SectorCreateView.as_view(), name="sector-create"),
    path('settori/<int:pk>/', views.sector_detail_view, name="sector-detail"),
    path('settori/modifica/<int:pk>/', views.SectorUpdateView.as_view(), name="sector-update"),
    path('settori/cancella/<int:pk>/', views.SectorDeleteView.as_view(), name="sector-delete"),

    path('staff/', views.StaffListView.as_view(), name="staff-list"),
    path('staff/crea/', views.StaffCreateView.as_view(), name="staff-create"),
    path('staff/<int:pk>/', views.staff_detail_view, name="staff-detail"),
    path('staff/modifica/<int:pk>/', views.StaffUpdateView.as_view(), name="staff-update"),
    path('staff/modifica/activate/<int:pk>/', views.staff_activate_view, name="staff-activate"),
    path('staff/cancella/<int:pk>/', views.StaffDeleteView.as_view(), name="staff-delete"),

    path('stage/', views.StageListView.as_view(), name="stage-list"),
    path('stage/crea/', views.StageCreateView.as_view(), name="stage-create"),
    path('stage/<int:pk>/', views.stage_detail_view, name="stage-detail"),
    path('stage/convention/<int:stage>_<int:student>/', views.stage_convention_detail_view, name="stage-convention-detail"),
    path('stage/modifica/<int:pk>/', views.StageUpdateView.as_view(), name="stage-update"),
    path('stage/cancella/<int:pk>/', views.StageDeleteView.as_view(), name="stage-delete"),

    path('studenti/', views.StudentListView.as_view(), name="student-list"),
    path('studenti/upload/', views.upload_csv, name="student-log-upload"),
    path('regione/upload/', views.upload_csv_regione_toscana, name="regione-upload-students"),
    path('studenti/list/upload/', views.upload_students_csv, name="student-list-upload"),
    path('studenti/crea/', views.StudentCreateView.as_view(), name="student-create"),
    path('studenti/<int:pk>/', views.student_detail_view, name="student-detail"),
    path('studenti/modifica/<int:pk>/', views.StudentUpdateView.as_view(), name="student-update"),
    path('studenti/cancella/<int:pk>/', views.StudentDeleteView.as_view(), name="student-delete"),

    path('staff/insegnanti/', views.TeacherListView.as_view(), name="teacher-list"),

    path('unita-formative/', views.TrainingUnitListView.as_view(), name="trainingunit-list"),
    path('unita-formative/crea/', views.TrainingUnitCreateView.as_view(), name="trainingunit-create"),
    path('unita-formative/<int:pk>/', views.training_unit_detail_view, name="trainingunit-detail"),
    path('unita-formative/modifica/<int:pk>/', views.TrainingUnitUpdateView.as_view(), name="trainingunit-update"),
    path('unita-formative/cancella/<int:pk>/', views.TrainingUnitDeleteView.as_view(), name="trainingunit-delete"),

    path('api/studenti/', views.StudentAPIListView.as_view(), name='api-view'),
    path('api/studenti/<slug:fiscal_code>/', views.StudentAPIDetailView.as_view(), name='api-detail-view'),
    path('api/studenti/note/<slug:fiscal_code>/', views.DisciplinaryMeasureAPIDetailView.as_view(), name='disciplinary-api-view'),
    path('api/studenti/note/<slug:fiscal_code>/<int:measure_id>/check/', views.DisciplinaryMeasureAPIUpdateView.as_view(), name='disciplinary-api-update-view'),

    path('api/studenti/comunicazioni/<slug:fiscal_code>/', views.CommunicationAPIListView.as_view(), name='communication-api-list-view'),
    path('api/studenti/comunicazioni/<slug:fiscal_code>/<int:pk>/', views.CommunicationAPIUpdateView.as_view(), name='communication-api-update-view'),

    path('api/login/', views.ExampleView.as_view(), name='api-login'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
]

#obtain_auth_token
