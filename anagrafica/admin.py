from django.contrib import admin
from .models import Classroom, Company, Communication, Convention, Course, CourseType, DisciplinaryMeasure, \
    DisciplinaryMeasureRead, Sector, Staff, Stage, Student, TrainingUnit

# class CurriculumModelAdmin(admin.ModelAdmin):
#     model = Course
#     list_display = ["name"]
#     search_fields = ["name", "category"]
#     list_filter = ["category"]


class StudentModelAdmin(admin.ModelAdmin):
    model = Student
    list_display = ["surname", "course"]
    search_fields = ["surname", "course"]
    list_filter = ["course"]

class CommunicationModelAdmin(admin.ModelAdmin):
    model = Communication
    list_filter = ["student__course"]


class DisciplinaryMeasureReadModelAdmin(admin.ModelAdmin):
    model = DisciplinaryMeasureRead
    list_display = ["student", "measure"]
    search_fields = ["student"]
    list_filter = ["student"]


class TrainingUnitModelAdmin(admin.ModelAdmin):
    model = TrainingUnit
    search_fields = ["course"]
    list_filter = ["course"]


admin.site.register(Classroom)
admin.site.register(Company)
admin.site.register(Communication, CommunicationModelAdmin)
admin.site.register(Convention)
admin.site.register(Course)
admin.site.register(CourseType)
admin.site.register(DisciplinaryMeasure)
admin.site.register(DisciplinaryMeasureRead)
admin.site.register(Sector)
admin.site.register(Staff)
admin.site.register(Stage)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(TrainingUnit, TrainingUnitModelAdmin)

