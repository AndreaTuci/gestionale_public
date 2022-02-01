from django.db import models
from anagrafica.models import Staff, TrainingUnit, Student
from django_countries.fields import CountryField
from django.urls import reverse
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from core.models import User
from anagrafica.models import Classroom, Course, TrainingUnit
from amministrazione.models import TeacherAgreement


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Staff,
                                on_delete=models.CASCADE,
                                related_name="reference_teacher",
                                verbose_name="Docente"
                                )

    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name="teacher_reference_unit",
                                      verbose_name="UF"
                                      )

    attendance_date = models.DateField(default=datetime.now,
                                       verbose_name="Data")

    class Meta:
        verbose_name = "Presenza docente"
        verbose_name_plural = "Presenze docente"

    def __str__(self):
        return self.teacher.surname + " (" + self.training_unit.name + ") del " + str(self.attendance_date)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name="reference_student",
                                verbose_name="Allievo"
                                )

    attendance_date = models.DateField(default=datetime.now,
                                       verbose_name="Data")

    EVENT = (
        ('P', 'Presente'),
        ('R', 'Ritardo'),
        ('G', 'Ritardo giustificato'),
        ('U', 'Uscita anticipata'),
        ('A', 'Assente'),
        ('RU', 'Ritardo e uscita ant.'),
        ('S', 'Sospensione'),
        ('F', 'Ore perse in FAD')
    )

    event = models.CharField(max_length=50,
                             choices=EVENT,
                             default='P',
                             verbose_name="Evento")

    hours_lost = models.PositiveSmallIntegerField(default=0,
                                                  validators=[MaxValueValidator(8), MinValueValidator(0)],
                                                  verbose_name="Ore perse")

    class Meta:
        verbose_name = "Presenza allievo"
        verbose_name_plural = "Presenze allievo"

    def __str__(self):
        return self.student.surname + " " + self.student.name + " (" + str(self.attendance_date) + ")"


class Note(models.Model):
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name="student_with_note",
                                verbose_name="Studente",
                                blank=True,
                                null=True,
                                )

    reminder = models.BooleanField(default=False,
                                   verbose_name='Promemoria')

    reminder_date = models.DateField(default=datetime.now,
                                     blank=True,
                                     null=True,
                                     verbose_name="Data promemoria")

    priority = models.BooleanField(default=False,
                                   verbose_name="Importante")

    note_text = models.CharField(max_length=280,
                                 verbose_name="Testo")

    solved = models.BooleanField(default=False,
                                 verbose_name="Risolto")

    created_by = models.ForeignKey(User,
                                   on_delete=models.DO_NOTHING,
                                   related_name='creator_user',
                                   verbose_name='Creata da')

    created_at = models.DateField(default=datetime.now,
                                  verbose_name="Data di creazione")

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Note"

    def __str__(self):
        return self.student.surname + " " + self.student.name + " (" + str(self.created_at) + ")"


class FamilyCommunication(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name="communication_reference_course",
                               verbose_name="Corso"
                               )
    year = models.PositiveSmallIntegerField(verbose_name='Anno')
    month = models.PositiveSmallIntegerField(verbose_name='Mese')
    text = models.TextField(blank=True, verbose_name='Comunicazioni')

    class Meta:
        verbose_name = "Comunicazione"
        verbose_name_plural = "Comunicazioni"

    def __str__(self):
        return "Comunicazioni per " + self.course.name + " di " + str(self.month) + "/" + str(self.year)


class Lesson(models.Model):
    DAYS = [
        ('Lun', 'Lunedì'),
        ('Mar', 'Martedì'),
        ('Mer', 'Mercoledì'),
        ('Gio', 'Giovedì'),
        ('Ven', 'Venerdì')
    ]
    HOURS = [
        (1, '08.00-09.00'),
        (2, '09.00-10.00'),
        (3, '10.00-11.00'),
        (4, '11.00-12.00'),
        (5, '12.00-13.00'),
        (6, '13.00-14.00'),
        (7, '14.00-15.00'),
        (8, '15.00-16.00'),
        (9, '16.00-17.00'),
    ]
    day = models.CharField(max_length=12,
                           choices=DAYS,
                           verbose_name='Giorno')
    hour = models.IntegerField(
        choices=HOURS,
        verbose_name='Ora')

    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name='uf_related_lesson',
                                      verbose_name='Unità Formativa')

    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name='classroom_for_lesson',
                                  verbose_name='Aula')

    def get_teacher(self):
        uf = self.training_unit
        contract = TeacherAgreement.objects.filter(training_unit=uf)
        return f'{contract.last().employee.name[0]}. {contract.last().employee.surname}'

    class Meta:
        verbose_name = 'Lezione'
        verbose_name_plural = 'Lezioni'
        # unique_together = ['day', 'hour', 'training_unit']

    def __str__(self):
        return f'{self.training_unit.course.name} - Lezione di {self.day} ore {self.hour}'


class LessonWithDate(models.Model):
    HOURS = [
        (1, '08.00-09.00'),
        (2, '09.00-10.00'),
        (3, '10.00-11.00'),
        (4, '11.00-12.00'),
        (5, '12.00-13.00'),
        (6, '13.00-14.00'),
        (7, '14.00-15.00'),
        (8, '15.00-16.00'),
        (9, '16.00-17.00'),
    ]
    lesson_date = models.DateField(verbose_name='Data della lezione')

    hour = models.IntegerField(
        choices=HOURS,
        verbose_name='Ora')

    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name='uf_lesson_with_date',
                                      verbose_name='Unità Formativa')

    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name='classroom_lesson_with_date',
                                  verbose_name='Aula')

    def get_teacher(self):
        uf = self.training_unit
        contract = TeacherAgreement.objects.filter(training_unit=uf)
        return f'{contract.last().employee.name[0]}. {contract.last().employee.surname}'

    def check_if_validate(self):
        try:
            validate = LessonDone.objects.get(related_lesson=self)
        except:
            validate = None
        return validate is not None

    class Meta:
        verbose_name = 'Lezione con data'
        verbose_name_plural = 'Lezioni con data'
        unique_together = ['lesson_date', 'hour', 'training_unit']

    def __str__(self):
        return f'{self.training_unit.course.name} - {self.training_unit.name} del {self.lesson_date} - ore {self.hour}'


class LessonDone(models.Model):
    HOURS = [
            (1, '08.00-09.00'),
            (2, '09.00-10.00'),
            (3, '10.00-11.00'),
            (4, '11.00-12.00'),
            (5, '12.00-13.00'),
            (6, '13.00-14.00'),
            (7, '14.00-15.00'),
            (8, '15.00-16.00'),
            (9, '16.00-17.00'),
        ]

    lesson_date = models.DateField(verbose_name='Data della lezione')

    hour = models.IntegerField(
        choices=HOURS,
        verbose_name='Ora')

    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name='uf_lesson_done',
                                      verbose_name='Unità Formativa')

    teacher = models.ForeignKey(Staff,
                                on_delete=models.CASCADE,
                                related_name='teacher_lesson_done',
                                verbose_name='Docente')

    related_lesson = models.ForeignKey(LessonWithDate,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       related_name='related_lesson_in_schedule',
                                       verbose_name='Lezione relativa in orario')

    class Meta:
        verbose_name = 'Lezione svolta'
        verbose_name_plural = 'Lezioni svolte'
        unique_together = ['lesson_date', 'hour', 'training_unit']

    def __str__(self):
        return f'{self.training_unit.course.name} - {self.training_unit.name} del {self.lesson_date} - ore {self.hour}'


class LessonSend(models.Model):
    day = models.CharField(max_length=12,
                           verbose_name='Giorno')
    hour = models.CharField(max_length=12,
                            verbose_name='Ora')
    training_unit = models.ForeignKey(TrainingUnit,
                                      on_delete=models.CASCADE,
                                      related_name='uf_send_related_lesson',
                                      verbose_name='Unità Formativa')

    def get_teacher(self):
        uf = self.training_unit
        contract = TeacherAgreement.objects.filter(training_unit=uf)
        return f'{contract.last().employee.name[0]}. {contract.last().employee.surname}'

    class Meta:
        verbose_name = 'Lezione inviata'
        verbose_name_plural = 'Lezioni inviate'
        # unique_together = ['day', 'hour', 'training_unit']

    def __str__(self):
        return f'{self.training_unit.course.name} - Lezione di {self.day} ore {self.hour}'
