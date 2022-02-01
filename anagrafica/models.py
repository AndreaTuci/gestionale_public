import random

from django.db import models
# from django_countries.fields import CountryField
from django.urls import reverse
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Sector(models.Model):
    sector_name = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name="Settore")
    stage_objectives = models.TextField(verbose_name="Obiettivi stage",
                                        blank=True)

    class Meta:
        verbose_name = "Settore"
        verbose_name_plural = "Settori"
        ordering = ['sector_name']

    def __str__(self):
        return self.sector_name


class Classroom(models.Model):
    name = models.CharField(max_length=25,
                            unique=True,
                            verbose_name="Nome dell'aula")

    schedule_name = models.CharField(max_length=15,
                                     null=True,
                                     unique=True,
                                     help_text='Es. LAB-ELE1',
                                     verbose_name="Nome per orario")

    def __str__(self):
        return f'{self.schedule_name} ({self.name})'

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aule"


class Company(models.Model):
    sector = models.ForeignKey(Sector,
                               on_delete=models.CASCADE,
                               related_name="company_reference_sector",
                               verbose_name="Settore di riferimento",
                               )

    name = models.CharField(max_length=70,
                            unique=True,
                            verbose_name="Ragione sociale")

    # vat = models.CharField(max_length=35,
    #                        # unique=True,
    #                        verbose_name="P. IVA",
    #                        blank=True,  # poi levalo
    #                        null=True,  # poi levalo
    #                        )

    # commerce_registration = models.CharField(max_length=35,
    #                                          # unique=True,
    #                                          verbose_name="Iscrizione Camera di Commercio N°",
    #                                          blank=True,  # poi levalo
    #                                          null=True,  # poi levalo
    #                                          )
    #
    # registered_office_city = models.CharField(max_length=100,
    #                                           verbose_name="Sede legale - Comune",
    #                                           blank=True,  # poi levalo
    #                                           null=True,  # poi levalo
    #                                           )
    #
    # registered_office_address = models.CharField(max_length=100,
    #                                              verbose_name="Sede legale - Indirizzo",
    #                                              blank=True,  # poi levalo
    #                                              null=True,  # poi levalo
    #                                              )

    operational_headquarters_city = models.CharField(max_length=100,
                                                     verbose_name="Sede operativa - Comune",
                                                     blank=True,  # poi levalo
                                                     null=True,  # poi levalo
                                                     )

    operational_headquarters_address = models.CharField(max_length=100,
                                                        verbose_name="Sede operativa - Indirizzo",
                                                        blank=True,  # poi levalo
                                                        null=True,  # poi levalo
                                                        )

    chief_legal_surname = models.CharField(max_length=100,
                                           verbose_name="Responsabile legale",
                                           blank=True,  # poi levalo
                                           null=True,  # poi levalo
                                           )

    # chief_legal_name = models.CharField(max_length=100,
    #                                     verbose_name="RL - Nome",
    #                                     blank=True,  # poi levalo
    #                                     null=True,  # poi levalo
    #                                     )

    # YEAR_CHOICES = [(r, r) for r in range(1920, datetime.now().year)]
    #
    # chief_legal_birth = models.IntegerField(choices=YEAR_CHOICES,
    #                                     verbose_name="Responsabile legale - Nome")

    # chief_legal_birth = models.DateField(verbose_name="RL - Data di nascita",
    #                                      blank=True,  # poi levalo
    #                                      null=True,  # poi levalo
    #                                      )
    #
    # chief_legal_place_of_birth = models.CharField(max_length=100,
    #                                               verbose_name="RL - Nato a",
    #                                               blank=True,  # poi levalo
    #                                               null=True,  # poi levalo
    #                                               )
    #
    # chief_legal_role = models.CharField(max_length=100,
    #                                     verbose_name="RL - In qualità di",
    #                                     blank=True,  # poi levalo
    #                                     null=True,  # poi levalo
    #                                     )
    #
    # chief_legal_resident_in = models.CharField(max_length=100,
    #                                            verbose_name="RL - Residente in",
    #                                            blank=True,  # poi levalo
    #                                            null=True,  # poi levalo
    #                                            )

    company_contact = models.CharField(max_length=100,
                                       verbose_name="Referente aziendale",
                                       blank=True,  # poi levalo
                                       null=True,  # poi levalo
                                       )

    email = models.EmailField(max_length=100,
                              blank=True,
                              null=True,
                              verbose_name="E-mail")

    telephone = models.CharField(max_length=50,
                                 blank=True,
                                 null=True,
                                 verbose_name="Telefono")

    class Meta:
        verbose_name = "Ditta"
        verbose_name_plural = "Ditte"

    def __str__(self):
        return self.name


class CourseType(models.Model):
    course_type = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name="Tipologia")

    def __str__(self):
        return self.course_type

    class Meta:
        verbose_name = "Tipologia di corso"
        verbose_name_plural = "Tipologie di corso"
        ordering = ['course_type']


class Course(models.Model):
    type = models.ForeignKey(CourseType,
                             on_delete=models.CASCADE,
                             related_name="type_course",
                             verbose_name="Tipo di corso"
                             )

    sector = models.ForeignKey(Sector,
                               on_delete=models.CASCADE,
                               related_name="reference_sector",
                               verbose_name="Settore di riferimento"
                               )

    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name="Nome del corso")

    official_name = models.CharField(max_length=128,
                                     null=True,
                                     blank=True,
                                     verbose_name="Nome ufficiale del corso")

    tutor = models.CharField(max_length=30,
                             blank=True,
                             null=True,
                             verbose_name="Tutor")

    start_date = models.DateField(default=datetime.now,
                                  verbose_name="Data di inizio")

    expected_end_date = models.DateField(default=datetime.now,
                                         verbose_name="Data prevista conclusione")

    is_finished = models.BooleanField(default=False,
                                      verbose_name='Corso concluso')

    actual_end_date = models.DateField(default=datetime.now,
                                       blank=True,
                                       null=True,
                                       verbose_name="Data effettiva conclusione")

    duration = models.PositiveSmallIntegerField(verbose_name="Durata in ore")

    classroom_h = models.PositiveSmallIntegerField(verbose_name="Ore di aula")

    stage_h = models.PositiveSmallIntegerField(verbose_name="Ore di stage")

    def clean(self):
        if self.duration != (self.classroom_h + self.stage_h):
            raise ValidationError(
                {'duration': 'La somma delle ore di aula e ore di stage non coincide con il totale.'})

    def __str__(self):
        return self.name

    def get_students(self):
        return Student.objects.filter(course=self).order_by("surname")

    def todays_attendances_exists(self):
        student = Student.objects.filter(course=self, is_withdrawn=False).first()
        try:
            if student.get_today_attendance_existance():
                attendances_exists = True
            else:
                attendances_exists = False
        except:
            attendances_exists = False
        return attendances_exists

    def get_students_count(self):
        return len(Student.objects.filter(course=self))

    def get_disciplinay_measures_count(self):
        measures = 0
        for student in self.get_students():
            student_measures = Student.get_disciplinary_measures_count(student)
            measures += student_measures
        return measures

    def get_absolute_url(self):
        return reverse("course-detail", kwargs={"pk": self})

    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"
        ordering = ['type', 'sector', 'name']


class Student(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Nome")

    surname = models.CharField(max_length=50,
                               verbose_name="Cognome")

    photo = CloudinaryField('photo',
                            folder='students_photos',
                            blank=True,
                            null=True,
                            )

    date_of_birth = models.DateField(default=datetime.now,
                                     verbose_name="Data di nascita")

    place_of_birth = models.CharField(max_length=50,
                                      verbose_name="Luogo di nascita",
                                      blank=True,
                                      null=True,
                                      )

    resident_in_city = models.CharField(max_length=50,
                                        verbose_name="Città di residenza")

    resident_in_address = models.CharField(max_length=50,
                                           verbose_name="Indirizzo di residenza")

    postal_code = models.CharField(max_length=5,
                                   verbose_name="CAP",
                                   blank=True,
                                   null=True,
                                   )

    fiscal_code = models.CharField(max_length=16,
                                   unique=True,
                                   verbose_name="C.F.",
                                   blank=True,
                                   null=True,
                                   )

    handicap = models.BooleanField(verbose_name="Portatore di handicap",
                                   blank=True,
                                   null=True,
                                   )

    email = models.EmailField(max_length=50,
                              blank=True,
                              null=True,
                              verbose_name="Email")

    telephone = models.CharField(max_length=20,
                                 blank=True,
                                 null=True,
                                 verbose_name="Telefono")

    parent_email_1 = models.EmailField(max_length=50,
                                       blank=True,
                                       null=True,
                                       verbose_name="Email di riferimento (1)")

    parent_telephone_1 = models.CharField(max_length=20,
                                          blank=True,
                                          null=True,
                                          verbose_name="Telefono di riferimento (1)")

    parent_role_1 = models.CharField(max_length=20,
                                     blank=True,
                                     null=True,
                                     verbose_name="Ruolo del riferimento (1)")

    parent_email_2 = models.EmailField(max_length=50,
                                       blank=True,
                                       null=True,
                                       verbose_name="Email di riferimento (2)")

    parent_telephone_2 = models.CharField(max_length=20,
                                          blank=True,
                                          null=True,
                                          verbose_name="Telefono di riferimento (2)")

    parent_role_2 = models.CharField(max_length=20,
                                     blank=True,
                                     null=True,
                                     verbose_name="Ruolo del riferimento (2)")

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name="attended_curriculum",
                               verbose_name="Corso frequentato",
                               )

    number = models.PositiveSmallIntegerField(default=1,
                                              verbose_name="Numero sul registro")

    registration_date = models.DateField(default=datetime.now,
                                         verbose_name="Data di iscrizione",
                                         blank=True,
                                         null=True)

    is_withdrawn = models.BooleanField(default=False,
                                       verbose_name='Ritirato')

    withdrawal_date = models.DateField(blank=True,
                                       null=True,
                                       verbose_name="Data di ritiro")

    WITHDRAWAL_CAUSE = (
        ('C', 'Cambio di attività formativa'),
        ('L', 'Ingresso nel mondo del lavoro'),
        ('A', 'Abbandono'),
        ('E', 'Espulsione'),
    )

    withdrawal_cause = models.CharField(max_length=50,
                                        choices=WITHDRAWAL_CAUSE,
                                        blank=True,
                                        null=True,
                                        verbose_name="Causa del ritiro")

    qualification_date = models.DateField(blank=True,
                                          null=True,
                                          verbose_name="Data di qualifica")

    grade = models.PositiveSmallIntegerField(blank=True,
                                             null=True,
                                             verbose_name="Voto di qualifica")

    postponed_entry = models.CharField(max_length=63,
                                       blank=True,
                                       null=True,
                                       verbose_name="Entrata posticipata")

    early_exit = models.CharField(max_length=63,
                                  blank=True,
                                  null=True,
                                  verbose_name="Uscita anticipata")

    delays = models.PositiveSmallIntegerField(default=0,
                                              verbose_name="Numero di ritardi")

    notes = models.TextField(blank=True,
                             verbose_name="Note")

    def __str__(self):
        return self.surname + " " + self.name  # + " - " + self.course.name

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})

    def get_disciplinary_measures(self):
        disciplinary_measures = DisciplinaryMeasure.objects.filter(students=self)
        return disciplinary_measures

    def get_disciplinary_measures_count(self):
        return len(DisciplinaryMeasure.objects.filter(students=self))

    def get_absences_number(self):
        absences = [0, 0, 0, 0, 0]
        for attendance in self.reference_student.all():
            if attendance.event in ['A', 'S']:
                absences[0] += 1
            elif attendance.event in ['R']:
                absences[1] += 1
            elif attendance.event in ['U']:
                absences[2] += 1
            elif attendance.event in ['RU', 'F']:
                absences[3] += 1
            elif attendance.event in ['G']:
                absences[4] += 1
        return absences

    def get_attendances(self):
        attendances = [0, 0]
        for attendance in self.reference_student.all():
            if attendance.event in ['A', 'S']:
                attendances[0] += 1
            else:
                attendances[1] += 1

        max_attendances = attendances[0] + attendances[1]

        if max_attendances == 0:
            max_attendances = 1
            attendances[1] = 1

        attendances[0] = round(attendances[0] / max_attendances, 2)
        attendances[1] = round(attendances[1] / max_attendances, 2)
        return attendances

    def get_today_attendance_existance(self):
        attendance_exists = False
        for attendance in self.reference_student.all():
            if datetime.now().date() == attendance.attendance_date:
                attendance_exists = True
        return attendance_exists

    def get_today_attendance_value(self):
        attendance_value = ''
        for attendance in self.reference_student.all():
            if datetime.now().date() == attendance.attendance_date:
                attendance_value = attendance.get_event_display()
        return attendance_value

    class Meta:
        verbose_name = "Studente"
        verbose_name_plural = "Studenti"
        ordering = ['surname']


class Staff(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)

    avatar = CloudinaryField('avatar',
                             folder='avatars',
                             blank=True,
                             null=True,
                             )

    surname = models.CharField(max_length=50,
                               verbose_name="Cognome")

    name = models.CharField(max_length=50,
                            verbose_name="Nome")

    date_of_birth = models.DateField(default=datetime.now,
                                     verbose_name="Data di nascita")

    place_of_birth = models.CharField(max_length=50,
                                      verbose_name="Luogo di nascita")

    resident_in_city = models.CharField(max_length=50,
                                        verbose_name="Città di residenza")

    resident_in_address = models.CharField(max_length=50,
                                           verbose_name="Indirizzo di residenza")

    postal_code = models.CharField(max_length=5,
                                   verbose_name="CAP")

    fiscal_code = models.CharField(max_length=16,
                                   unique=True,
                                   verbose_name="C.F.")

    vat = models.CharField(max_length=35,
                           unique=True,
                           blank=True,
                           null=True,
                           verbose_name="P. IVA")

    email = models.EmailField(max_length=50,
                              blank=True,
                              null=True,
                              verbose_name="E-mail")

    telephone = models.CharField(max_length=20,
                                 blank=True,
                                 null=True,
                                 verbose_name="Telefono")

    curriculum = CloudinaryField('cv',
                                 resource_type="auto",
                                 folder='CV',
                                 blank=True,
                                 null=True,
                                 )

    INPS = CloudinaryField('inps',
                           folder='INPS',
                           blank=True,
                           null=True,
                           )

    IRPEF = CloudinaryField('irpef',
                            folder='IRPEF',
                            blank=True,
                            null=True,
                            )

    TASKS = (
        ('A', 'Altro'),
        ('D', 'Docente'),
        ('T', 'Tutor'),
        ('S', 'Segreteria'),
        ('C', 'Coordinamento'),
        ('P', 'Direzione'),
    )

    task = models.CharField(max_length=20,
                            choices=TASKS,
                            verbose_name="Mansione")

    active = models.BooleanField(default=False,
                                 verbose_name="Utente attivo")

    badge = models.SlugField(max_length=25,
                             blank=True,
                             null=True,
                             unique=True,
                             verbose_name='Codice badge')

    class Meta:
        verbose_name = "Personale"
        verbose_name_plural = "Personale"
        ordering = ['surname']

    def __str__(self):
        return f'{self.surname} {self.name}'

    def save(self, *args, **kwargs):
        if self.badge != self.generate_badge_code():
            self.badge = self.generate_badge_code()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})

    def generate_badge_code(self):
        name = ''
        add = ''
        task = self.get_task_display()
        i = 0
        birth_date = datetime(self.date_of_birth.year, self.date_of_birth.month, self.date_of_birth.day)
        birth_date = datetime.strftime(birth_date, '%d%m%Y')
        while len(name) <= 25:
            if i < len(self.name):
                add = add + self.name[i]
            if i < len(self.surname):
                add = add + self.surname[i]
            if i < len(birth_date):
                add = add + task[i]
            if i % 3 == 0:
                add = add.upper()
            name = name + add + str(i)
            i += 1
        name = name[:25]
        badge = name
        badges_already_in = list(Staff.objects.filter(badge__in = [employee.badge for employee in Staff.objects.all()]).values_list('badge', flat=True))
        i = 0
        while True:
            if badge in badges_already_in:
                if Staff.objects.get(badge__exact=badge).pk == self.pk:
                    break
                badge = badge[:-1]
                badge = badge + badge[i]
                i += 1
            else:
                break
        return badge


class Communication(models.Model):
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name="comunicazione_per",
                                verbose_name="Allievo"
                                )
    subject = models.CharField(max_length=127,
                               verbose_name="Oggetto")

    content = models.TextField(verbose_name="Contenuto")

    created_at = models.DateField(default=datetime.now,
                                  verbose_name="Data di creazione")

    read_by_family = models.BooleanField(default=False,
                                         verbose_name="Letta dalla famiglia")

    date_of_reading = models.DateField(null=True,
                                       blank=True,
                                       verbose_name="Letta in data")

    def __str__(self):
        return f'Comunicazione del {self.created_at} per {str(self.student.surname)} [{self.subject[:30]}]'

    class Meta:
        verbose_name = "Comunicazione alla famiglia"
        verbose_name_plural = "Comunicazioni alle famiglie"
        ordering = ['-created_at']


class DisciplinaryMeasure(models.Model):
    students = models.ManyToManyField(Student,
                                      default="",
                                      blank=True,
                                      verbose_name="Allievi"
                                      )

    NOTES = (
        ('COLLOQUIO', 'Colloquio con tutor'),
        ('DIREZIONE', 'Colloquio con preside'),
        ('FAMIGLIA', 'Incontro con famiglia'),
        ('SOSPENSIONE', 'Sospensione'),
    )

    note_type = models.CharField(max_length=20,
                                 choices=NOTES,
                                 verbose_name="Proposta")

    reporting_date = models.DateField(default=datetime.now,
                                      verbose_name="Data di segnalazione")

    teacher_reporting = models.ForeignKey(Staff,
                                          on_delete=models.CASCADE,
                                          default="Docente non in elenco",
                                          blank=True,
                                          null=True,
                                          related_name="teacher_reporting",
                                          verbose_name="Docente"
                                          )

    tutor_reporting = models.ForeignKey(Staff,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        related_name="tutor_reporting",
                                        verbose_name="Tutor"
                                        )

    motivation = models.TextField(verbose_name="Motivazione")

    def __str__(self):
        return f'{self.note_type} del {str(self.reporting_date)} [{self.motivation[:30]}'

    class Meta:
        verbose_name = "Provvedimento disciplinare"
        verbose_name_plural = "Provvedimenti disciplinari"
        ordering = ['-reporting_date']


class DisciplinaryMeasureRead(models.Model):
    measure = models.CharField(max_length=10,
                               verbose_name="Segnalazione"
                               )

    student = models.CharField(max_length=16,
                               verbose_name="Studente"
                               )

    created_at = models.DateField(default=datetime.now,
                                  verbose_name="Data di creazione")

    def __str__(self):
        return f'[{self.pk}] {self.student} ha letto la segnalazione n. {self.measure}'

    class Meta:
        unique_together = [['measure', 'student']]
        verbose_name = "Lettura segnalazione"
        verbose_name_plural = "Letture segnalazioni"


class TrainingUnit(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name="reference_course",
                               verbose_name="Corso"
                               )

    code = models.PositiveSmallIntegerField(verbose_name="Codice")

    name = models.CharField(max_length=50,
                            verbose_name="Nome")

    hours_expected = models.PositiveSmallIntegerField(verbose_name="Ore previste")

    hours_remaining = models.PositiveSmallIntegerField(default=hours_expected,
                                                       verbose_name="Ore residue")

    KINDS = [
        ('L', 'Laboratorio'),
        ('U', 'Teoria, materie umanistiche'),
        ('T', 'Teoria, materie pratiche'),
    ]

    kind = models.CharField(max_length=1,
                            choices=KINDS,
                            default='U',
                            verbose_name='Tipo di materia')

    # qua è da pensare un controllo, che guardi alla somma delle ore UF previste,
    # le sommi e le confronti con le ore di aula previste per il corso

    class Meta:
        verbose_name = "Unità formativa"
        verbose_name_plural = "Unità formative"
        ordering = ['code']

    # def get_teacher:


    def __str__(self):
        return f'UF{str(self.code)} - {self.name} ({self.course.name})'


class Stage(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='course_in_stage',
                               verbose_name='Corso')
    start_date = models.DateField(verbose_name='Data di inizio')
    end_date = models.DateField(verbose_name='Data di fine')
    tutor = models.ForeignKey(Staff,
                              on_delete=models.CASCADE,
                              related_name='stage_tutor',
                              limit_choices_to={'task': 'T'},
                              null=True,
                              verbose_name='Tutor')
    medical_examination_date = models.DateField(verbose_name='Data visita medica',
                                                blank=True,
                                                null=True)
    medical_examination_renoval_date = models.DateField(verbose_name='Data rinnovo visita medica',
                                                        blank=True,
                                                        null=True)

    safety_certificate_date = models.DateField(verbose_name='Data attestato sicurezza',
                                               blank=True,
                                               null=True)

    re_entries = models.TextField(verbose_name="Rientri a scuola",
                                  blank=True)

    holidays = models.CharField(max_length=256,
                                blank=True,
                                verbose_name='Periodo di vacanze')

    def __str__(self):
        return f'Stage {self.course} dal {self.start_date} al {self.end_date}'

    class Meta:
        verbose_name = 'Stage'
        verbose_name_plural = 'Stage'


class Convention(models.Model):
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="affiliated_company",
                                verbose_name="Ditta")

    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name="affiliated_student",
                                verbose_name="Studente")

    date = models.DateField(default=datetime.now,
                            verbose_name="Data di stipula")

    begin = models.DateField(verbose_name="Data di inizio")

    end = models.DateField(verbose_name="Data di conclusione")

    company_tutor = models.CharField(max_length=30,
                                     verbose_name="Tutor aziendale")

    school_tutor = models.CharField(max_length=30,
                                    verbose_name="Tutor scolastico")

    # selezione da fare in base a Staff > Tutor
    schedule = models.TextField(verbose_name="Orario")

    return_hour = models.CharField(max_length=30,
                                   default="Dalle 8.00 alle 14.00",
                                   verbose_name="Orario nei giorni di rientro")

    return_day_one = models.DateField(verbose_name="Giorno di rientro 1",
                                      blank=True,
                                      null=True)

    return_day_two = models.DateField(verbose_name="Giorno di rientro 2",
                                      blank=True,
                                      null=True)

    return_day_three = models.DateField(verbose_name="Giorno di rientro 3",
                                        blank=True,
                                        null=True)

    class Meta:
        verbose_name = "Convenzione"
        verbose_name_plural = "Convenzioni"
        ordering = ['date']

    def get_absolute_url(self):
        return reverse("convention-detail", kwargs={"pk": self.pk})
