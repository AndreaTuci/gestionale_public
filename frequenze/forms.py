from django import forms
from .models import *
from datetime import datetime, timedelta
from amministrazione.models import TeacherAgreement
from django.contrib import messages
import itertools


class DateInput(forms.DateInput):
    input_type = 'date'
    # template_name = 'utils/date.html'

    # default = datetime.now


class CommunicationModelForm(forms.ModelForm):
    class Meta:
        model = FamilyCommunication
        exclude = ['year', 'month', 'course']
        labels = {
            'text': 'Comunicazioni'
        }


class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['created_at', 'created_by', 'solved']
        widgets = {
            'note_text': forms.Textarea
        }
        labels = {
            'solved': 'Situazione risolta [Archivia nota]',
        }


class TeacherAttendanceModelForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = "__all__"

    def __init__(self, teacher, uf, date, *args, **kwargs):
        super(TeacherAttendanceModelForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = teacher
        self.fields['training_unit'] = uf
        self.fields['attendance_date'] = date


class StudentAttendanceModelForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        exclude = ['hours_lost']
        # fields = "__all__"

        widgets = {
            'attendance_date': forms.DateInput(attrs={'readonly': 'readonly'}),
            # QUESTO E' QUI PER PROVARE AD ASSEGNARE UN VALORE A STUDENT

        }

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course')
        self.date = kwargs.pop('date')
        super(StudentAttendanceModelForm, self).__init__(*args, **kwargs)
        # course = Student.objects.filter(course=self.course)
        # self.fields['student'].queryset = course
        # self.fields['student'].widget.attrs['disabled'] = 'disabled'


BaseStudentAttendanceFormSet = forms.modelformset_factory(StudentAttendance, StudentAttendanceModelForm)


class StudentAttendanceFormSet(BaseStudentAttendanceFormSet):
    fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course')
        self.date = kwargs.pop('date')
        students = Student.objects.filter(course=self.course, is_withdrawn=False).order_by('number', 'surname', 'name')
        super(StudentAttendanceFormSet, self).__init__(*args, **kwargs)
        date_time_obj = datetime.strptime(self.date, '%Y-%m-%d')
        student_list = []
        attendandace_list_check = StudentAttendance.objects.filter(student__course=self.course,
                                                                   attendance_date=date_time_obj).order_by(
            'student__number')
        if attendandace_list_check:
            for attendance in attendandace_list_check:
                student_list.append({"student": attendance.student,
                                     "attendance_date": attendance.attendance_date,
                                     "event": attendance.event, })
                # "hours_lost": attendance.hours_lost})
            self.extra = 0

        else:
            self.extra = students.count()

            counter = 0
            while counter < students.count():
                student_list.append({"student": Student.objects.get(pk=students[counter].pk),
                                     "attendance_date": date_time_obj})
                counter += 1
            # self.initial={'student': '1'}
        self.initial = student_list

    def _construct_form(self, *args, **kwargs):
        kwargs['course'] = self.course
        kwargs['date'] = self.date
        return super(StudentAttendanceFormSet, self)._construct_form(*args, **kwargs)


class LessonModelForm(forms.ModelForm):

    def __init__(self, course, *args, **kwargs):
        #    try:
        #        self.course = kwargs.pop('course')
        #    except:
        #        self.course = 0
        super(LessonModelForm, self).__init__(*args, **kwargs)
        training_units = TrainingUnit.objects.filter(course=course)
        # self.fields['training_unit'].queryset = training_units
        self.fields['training_unit'].queryset = training_units.filter(contract_related_unit__isnull=False)
        # used_classrooms = set(lesson.classroom.schedule_name for lesson in Lesson.objects.all() if lesson.classroom.schedule_name)
        self.fields['classroom'].queryset = Classroom.objects.all()
        self.fields['day'].widget.attrs.update({'id': 'form_day'})
        self.fields['hour'].widget.attrs.update({'id': 'form_hour'})

    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {'classroom': forms.Select(attrs={'id': 'classroomID'})}

    def clean(self):
        classroom_ok = False
        cleaned_data = self.cleaned_data
        course = cleaned_data['training_unit'].course
        try:
            busy_teacher = TeacherAgreement.objects.get(training_unit=cleaned_data['training_unit']).employee
        except TeacherAgreement.DoesNotExist:
            raise ValidationError(f'Questa UF non ha nessun docente incaricato')
        try:
            teacher_agreements = TeacherAgreement.objects.filter(employee=busy_teacher)
            teacher_units = []
            for agreement in teacher_agreements:
                teacher_units.append(agreement.training_unit)
            scheduled_lesson = Lesson.objects.get(day=cleaned_data['day'],
                                                  hour=cleaned_data['hour'],
                                                  training_unit__in=teacher_units).training_unit.course
        except:
            pass
        else:
            raise ValidationError(f'All`ora scelta il docente ha già lezione con il corso {scheduled_lesson}')

        try:
            used_classrooms = set(
                lesson.classroom.schedule_name for lesson in Lesson.objects.filter(day=cleaned_data['day'],
                                                                                   hour=cleaned_data['hour']))
            choosed_classroom = cleaned_data['classroom']

        except:
            pass
        else:
            if choosed_classroom.schedule_name in used_classrooms:
                course_in_classroom = Lesson.objects.get(day=cleaned_data['day'],
                                                         hour=cleaned_data['hour'],
                                                         classroom__schedule_name=choosed_classroom.schedule_name).training_unit.course
                days = {'Lun': 'Lunedì',
                        'Mar': 'Martedì',
                        'Mer': 'Mercoledì',
                        'Gio': 'Giovedì',
                        'Ven': 'Venerdì'}
                hours = {1: 'dalle 8.00 alle 9.00',
                         2: 'dalle 9.00 alle 10.00',
                         3: 'dalle 10.00 alle 11.00',
                         4: 'dalle 11.00 alle 12.00',
                         5: 'dalle 12.00 alle 13.00',
                         6: 'dalle 13.00 alle 14.00',
                         7: 'dalle 14.00 alle 15.00',
                         8: 'dalle 15.00 alle 16.00',
                         9: 'dalle 16.00 alle 17.00',
                         }
                day = cleaned_data['day']
                hour = cleaned_data['hour']
                raise ValidationError(
                    f'Il {days[day]} {hours[hour]} l`aula {choosed_classroom} è già occupata dal corso {course_in_classroom}')

        try:
            lesson = Lesson.objects.get(day=cleaned_data['day'], hour=cleaned_data['hour'],
                                        training_unit__course=course.pk)
        except Lesson.DoesNotExist:
            pass
        else:
            raise ValidationError(f'All`ora scelta {course} ha già {lesson.training_unit.name}')

        # Always return cleaned_data
        return cleaned_data


class LessonWithDateModelForm(forms.ModelForm):

    def __init__(self, course, ref_date, *args, **kwargs):
        #    try:
        #        self.course = kwargs.pop('course')
        #    except:
        #        self.course = 0
        super(LessonWithDateModelForm, self).__init__(*args, **kwargs)
        self.ref_date = ref_date
        DAYS_CHOICES = [
            ('Lun', 'Lunedì'),
            ('Mar', 'Martedì'),
            ('Mer', 'Mercoledì'),
            ('Gio', 'Giovedì'),
            ('Ven', 'Venerdì'),
        ]
        training_units = TrainingUnit.objects.filter(course=course)
        self.fields['training_unit'].queryset = training_units.filter(contract_related_unit__isnull=False)
        self.fields['classroom'].queryset = Classroom.objects.all().order_by('name')
        self.fields['day'] = forms.ChoiceField(
            label='Giorno',
            required=True,
            widget=forms.Select,
            choices=DAYS_CHOICES,
    )
        self.fields['day'].widget.attrs.update({'id': 'form_day'})
        self.fields['hour'].widget.attrs.update({'id': 'form_hour'})

    class Meta:
        model = LessonWithDate
        exclude = ['lesson_date']
        widgets = {'day': forms.DateInput,
                  'classroom': forms.Select(attrs={'id': 'classroomID'})}

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        course = cleaned_data['training_unit'].course
        week_days = {
            'Lun': 'lunedì',
            'Mar': 'martedì',
            'Mer': 'mercoledì',
            'Gio': 'giovedì',
            'Ven': 'venerdì'}
        selected_day = week_days[cleaned_data['day']]
        ref_date = self.ref_date
        while True:
            if ref_date.strftime("%A") == selected_day:
                selected_day = ref_date
                break
            else:
                ref_date = ref_date + timedelta(days=1)

        try:
            busy_teacher = TeacherAgreement.objects.get(training_unit=cleaned_data['training_unit']).employee
        except TeacherAgreement.DoesNotExist:
            raise ValidationError(f'Questa UF non ha nessun docente incaricato')
        try:
            teacher_agreements = TeacherAgreement.objects.filter(employee=busy_teacher)
            teacher_units = []
            for agreement in teacher_agreements:
                teacher_units.append(agreement.training_unit)
            scheduled_lesson = LessonWithDate.objects.get(lesson_date=selected_day,
                                                          hour=cleaned_data['hour'],
                                                          training_unit__in=teacher_units).training_unit.course
        except:
            pass
        else:
            raise ValidationError(f'All`ora scelta {busy_teacher.name} {busy_teacher.surname} ha già lezione con il corso {scheduled_lesson}')

        try:
            used_classrooms = set(
                lesson.classroom.schedule_name for lesson in LessonWithDate.objects.filter(lesson_date=selected_day,
                                                                                   hour=cleaned_data['hour']))
            choosed_classroom = cleaned_data['classroom']

        except:
            pass
        else:
            if choosed_classroom.schedule_name in used_classrooms:
                course_in_classroom = LessonWithDate.objects.get(lesson_date=selected_day,
                                                         hour=cleaned_data['hour'],
                                                         classroom__schedule_name=choosed_classroom.schedule_name).training_unit.course
                days = {'Lun': 'Lunedì',
                        'Mar': 'Martedì',
                        'Mer': 'Mercoledì',
                        'Gio': 'Giovedì',
                        'Ven': 'Venerdì'}
                hours = {1: 'dalle 8.00 alle 9.00',
                         2: 'dalle 9.00 alle 10.00',
                         3: 'dalle 10.00 alle 11.00',
                         4: 'dalle 11.00 alle 12.00',
                         5: 'dalle 12.00 alle 13.00',
                         6: 'dalle 13.00 alle 14.00',
                         7: 'dalle 14.00 alle 15.00',
                         8: 'dalle 15.00 alle 16.00',
                         9: 'dalle 16.00 alle 17.00',
                         }
                day = cleaned_data['day']
                hour = cleaned_data['hour']
                raise ValidationError(
                    f'Il {days[day]} {hours[hour]} l`aula {choosed_classroom} è già occupata dal corso {course_in_classroom}')

        try:
            lesson = LessonWithDate.objects.get(lesson_date=selected_day, hour=cleaned_data['hour'],
                                        training_unit__course=course.pk)
        except LessonWithDate.DoesNotExist:
            pass
        else:
            raise ValidationError(f'All`ora scelta {course} ha già {lesson.training_unit.name}')

        # Always return cleaned_data
        return cleaned_data


class LessonDoneModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LessonDoneModelForm, self).__init__(*args, **kwargs)
        self.fields['training_unit'].queryset = TrainingUnit.objects.all().order_by('course__name', 'code')

    class Meta:
        model = LessonDone
        exclude = ['related_lesson']
        widgets = {
            'lesson_date': DateInput
        }


        # labels = {
        #     'solved': 'Situazione risolta [Archivia nota]',
        # }
