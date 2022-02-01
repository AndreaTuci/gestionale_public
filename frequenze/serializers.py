from .models import *
from rest_framework import serializers


class ScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    readable_uf = serializers.SerializerMethodField('get_uf')
    teacher = serializers.SerializerMethodField('get_teacher')

    def get_uf(self, obj):
        uf = obj.training_unit.name
        return uf

    def get_teacher(self, obj):
        lesson = LessonSend.objects.get(pk=obj.pk)
        teacher = lesson.get_teacher()
        return teacher

    class Meta:
        model = Lesson
        fields = '__all__'
