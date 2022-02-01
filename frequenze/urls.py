from django.urls import path
from . import graphs
from . import views

urlpatterns = [
    path('insegnanti/crea/teacher=<int:teacher>uf=<int:uf>date=<str:date>course=<int:course>/', views.teacher_attendance_create, name="teacherattendance-create"),

    path('lezioni/', views.LessonChoiceView.as_view(), name="lessonchoice"),
    path('lezioni/registro/', views.RegisterView.as_view(), name="register"),

    path('studenti/presenze/modifica/course=<int:course>date=<str:date>', views.student_attendance_create_view, name="studentattendance-create"),
    path('studenti/presenze/new/modifica/course=<int:course>date=<str:date>', views.student_new_attendance_create_view,
         name="studentattendance-new-create"),
    path('studenti/presenze/visualizza/course=<int:course>month=<int:month>year=<int:year>', views.student_attendance_course_list_view, name="studentattendance-course-list"),
    path('studenti/presenze/resetta-ritardi', views.reset_delays, name='reset-delays'),
    path('studenti/presenze/riconta-ritardi', views.count_delays, name='count-delays'),
    path('studenti/note/', views.NotesListView.as_view(), name="note-list"),
    path('studenti/note/<int:pk>/', views.notes_detail_view, name="note-detail"),
    path('studenti/note/crea/', views.NotesCreateView.as_view(), name="note-create"),
    path('studenti/note/modifica/<int:pk>', views.NoteUpdateView.as_view(), name="note-update"),
    path('studenti/note/cancella/<int:pk>', views.NotesDeleteView.as_view(), name="note-delete"),

    path('graphs/students/count/', graphs.StudentsPieChartJSONView.as_view(), name='students_pie_json'),
    path('graphs/students/measures/', graphs.DisciplinaryMeasuresPieChartJSONView.as_view(), name='measures_pie_json'),

    path('corsi/comunicazioni/', views.CommunicationCreateView.as_view(), name="communication-create"),
    path('corsi/comunicazioni/modifica/<int:course>-<int:pk>/', views.CommunicationUpdateView.as_view(), name="communication-update"),
    path('corsi/comunicazioni/elenco/<int:course>', views.CommunicationListView.as_view(), name="communication-list"),
    path('corsi/comunicazioni/<int:pk>/', views.communication_detail_view, name="communication-detail"),

    path('lezioni/crea/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lezioni/orario/aggiungi/<int:course>/', views.lesson_add, name='lesson-add'),
    path('lezioni/orario-con-date/aggiungi/course=<int:course>ref_date=<str:ref_date>/', views.new_lesson_add, name='new-lesson-add'),
    path('lezioni/orario/cancella/<int:pk>/', views.delete_lesson, name='lesson-delete'),
    path('lezioni/orario-con-date/cancella/pk=<int:pk>ref_date=<str:ref_date>/', views.new_delete_lesson, name='new-lesson-delete'),
    path('lezioni/orario/', views.lesson_choose_course, name='lesson-choose-course'),
    path('lezioni/orario-con-date/', views.new_lesson_choose_course, name='new-lesson-choose-course'),
    path('lezioni/orario-con-date/copia-orario/', views.copy_old_schedule, name='copy-schedule'),
    path('lezioni/orario/<int:course>/', views.lesson_schedule, name='lesson-schedule'),
    path('lezioni/orario-con-date/course=<int:course>ref_date=<str:ref_date>/', views.new_lesson_schedule, name='new-lesson-schedule'),
    path('lezioni/orario/invia/<int:course>/', views.send_schedule, name='send-schedule'),
    path('lezioni/orario/invia-a-tutti/', views.send_schedule_all_courses, name='send-schedule-all'),
    path('lezioni/orario-con-date/invia-a-tutti/ref_date=<str:ref_date>', views.new_send_schedule_all_courses, name='new-send-schedule-all'),
    path('lezioni/orario/invia/api/course=<int:course>/', views.ScheduleCourseAPIView.as_view(), name='api-send-schedule'),
    path('lezioni/orarione/', views.general_schedule, name='general-schedule'),
    path('lezioni/orarione-con-date/ref_date=<str:ref_date>/', views.new_general_schedule, name='new-general-schedule'),
    path('graphs/students/bar/<int:course>', graphs.AttendancesBarJSONView.as_view(), name='attendances_bar_json'),
    path('graphs/students/bar/general', graphs.GeneralAttendancesBarJSONView.as_view(), name='general-attendances_bar_json'),

    path('lezioni/orario-con-date/cancella-index/<int:pk>/', views.new_delete_lesson_to_index,
         name='new-lesson-delete-index'),
    path('lezioni/orario-con-date/valida/<int:pk>/', views.new_validate_lesson_to_index,
         name='new-lesson-validate-index'),
    path('lezioni/orario-con-date/valida-custom/', views.ValidateExtraLessonView.as_view(),
         name='validate-custom-lesson'),
    path('lezioni-validate/lista/', views.lesson_done_list_view,
         name='lesson-done-list'),

]
