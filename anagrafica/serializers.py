from .models import *
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    absences = serializers.SerializerMethodField('get_absences')
    attendances = serializers.SerializerMethodField('get_attendances')
    today_attendance = serializers.SerializerMethodField('get_today_attendance')
    photo_url = serializers.SerializerMethodField('get_photo_url')

    def get_attendances(self, obj):
        attendances = obj.get_attendances()
        return attendances

    def get_absences(self, obj):
        return obj.get_absences_number()

    def get_photo_url(self, obj):
        try:
            return obj.photo.url
        except:
            return ''

    def get_today_attendance(self, obj):
        return obj.get_today_attendance_value()

    class Meta:
        model = Student
        fields = '__all__'


class CommunicationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Communication
        fields = '__all__'


class DisciplinaryMeasureSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    humanized_note_type = serializers.SerializerMethodField('humanize_note_type')
    teacher = serializers.SerializerMethodField('get_teacher')
    tutor = serializers.SerializerMethodField('get_tutor')
    students_n = serializers.SerializerMethodField('get_students_number')
    already_read_by = serializers.SerializerMethodField('check_if_read')

    def check_if_read(self, obj):
        already_read = []
        students = []
        for student in obj.students.all():
            students.append(student.fiscal_code)

        students_who_read = DisciplinaryMeasureRead.objects.filter(measure=obj.id, student__in=students)
        for student in students_who_read:
            already_read.append(student.student)

        return already_read


    def humanize_note_type(self, obj):
        note = obj.get_note_type_display()
        return note

    def get_teacher(self, obj):
        teacher = ''
        if obj.teacher_reporting:
            teacher = f'{obj.teacher_reporting.name} {obj.teacher_reporting.surname}'
        return teacher

    def get_tutor(self, obj):
        tutor = ''
        if obj.tutor_reporting:
            tutor = f'{obj.tutor_reporting.name} {obj.tutor_reporting.surname}'
        return tutor

    def get_students_number(self, obj):
        return obj.students.count()

    class Meta:
        model = DisciplinaryMeasure
        fields = "__all__"


class DisciplinaryMeasureUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplinaryMeasureRead
        fields = '__all__'
