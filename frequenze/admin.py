from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance, Note, FamilyCommunication, \
    Lesson, LessonSend, LessonWithDate, LessonDone


class LessonModelAdmin(admin.ModelAdmin):
    model = Lesson
    list_filter = ["training_unit__course"]


class LessonWithDateModelAdmin(admin.ModelAdmin):
    model = LessonWithDate
    list_filter = ["training_unit__course", "lesson_date"]


class LessonDoneModelAdmin(admin.ModelAdmin):
    model = LessonDone
    list_filter = ["training_unit__course", "lesson_date"]


class LessonSendModelAdmin(admin.ModelAdmin):
    model = LessonSend
    list_filter = ["training_unit__course"]


class StudentAttendanceModelAdmin(admin.ModelAdmin):
    model = StudentAttendance
    list_filter = ["student__course", "event"]


admin.site.register(TeacherAttendance)
admin.site.register(Note)
admin.site.register(FamilyCommunication)
admin.site.register(Lesson, LessonModelAdmin)
admin.site.register(LessonSend, LessonSendModelAdmin)
admin.site.register(LessonDone, LessonDoneModelAdmin)
admin.site.register(LessonWithDate, LessonWithDateModelAdmin)
admin.site.register(StudentAttendance, StudentAttendanceModelAdmin)
