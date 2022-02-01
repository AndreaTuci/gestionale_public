from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
import random

from amministrazione.models import TimeCardEntry
from core.models import MotivationalPhrase
from core.forms import FirstAccessModelForm, CreateStudentUserForm
from frequenze.models import *
from datetime import timedelta
import sys
from core.utils import send_activation_mail, send_bug_mail
from core.auth_lists import BACKOFFICE
from django.contrib.auth.models import Group


def generate_barcodes(request):
    staff = Staff.objects.all()
    for employee in staff:
        employee.save()
    return redirect('index')


def index(request):
    tutor_data = {}
    secretary_data = {}
    if request.user.is_authenticated:
        post = ''
        if request.method == 'POST':
            barcode = request.POST.get('employee')
            staff = Staff.objects.all()
            try:
                employee = staff.get(badge=barcode)
                pk = employee.pk
                readable_in_out = 'Entrata'
                today_entries = TimeCardEntry.objects.filter(employee_id=pk, entry_date=datetime.now().date())
                if today_entries:
                    in_out = 'E'
                    if today_entries.last().in_out == 'E':
                        in_out = 'U'
                        readable_in_out = 'Uscita'
                    entry = TimeCardEntry(employee=employee,
                                          in_out=in_out)
                else:
                    entry = TimeCardEntry(employee=employee)
                entry.save()
                post = f'{employee.name} {employee.surname} - {readable_in_out}'
            except ObjectDoesNotExist:
                # return redirect(reverse('warehouse-movement-create', kwargs={'barcode': barcode}))
                post = 'errore'
        try:
            staff = Staff.objects.get(user=request.user)
            role = staff.get_task_display()
            avatar = staff.avatar
            active = staff.active
            if role == 'Tutor':
                tutor_data = get_tutor_data()
            elif role == 'Segreteria':
                secretary_data = get_secretary_data()
        except:
            role = ''
            avatar = ''
            active = False
        staff = Staff.objects.get(user_id=request.user.pk)
        context = {
            'backoffice': BACKOFFICE,
            'post': post,
            'month': datetime.now().date().month,
            'year': datetime.now().date().year,
            'age_control': datetime.now() - timedelta(weeks=int(52.1429*16)),
            'user_data': {'username': request.user.username,
                          'user_pk': staff.pk,
                          'user_barcode': staff.badge,
                          'first_name': request.user.first_name,
                          'last_name': request.user.last_name,
                          'email': request.user.email,
                          'role': role,
                          'avatar': avatar,
                          'tutor_data': tutor_data,
                          'secretary_data': secretary_data,
                          'active': active,
                          },
        }

        if MotivationalPhrase.objects.count() > 0:
            context['phrase'] = random.choice(MotivationalPhrase.objects.all())
        else:
            context['phrase'] = 'Sembra sempre impossibile, finché non viene fatto. (Nelson Mandela)'
        # context['address'] = 'https://www.google.it/maps/dir/Via+Pitoiese+Firenze/Via+Reginaldo+Giuliani+Firenze/'
        # context['address'] = 'https://www.google.it/maps/search/?api=1&query=elettricista+Via+Pitoiese+Firenze&z=19/'
        return render(request, 'index.html', context)
    else:
        context = {
            'user_data': 'None',
        }
        return render(request, 'index.html', context)


def logout(request):
    auth_logout(request)
    return redirect('/')


def create_student_user(request):
    if request.user.is_authenticated:
        form = CreateStudentUserForm
        context = {'message': '',
                   'form': form,
                   'error': '',
                   'list': []
                   }

        if request.method == 'POST':
            form = CreateStudentUserForm(data=request.POST)
            if form.is_valid():
                students_group = Group.objects.get(name='Studenti')
                course = Course.objects.get(name=form.cleaned_data['course'])
                for student in Student.objects.filter(course=course):
                    try:
                        if len(student.fiscal_code) == 16:
                            characters = ''
                            num_result = 0
                            nums = '0123456789'
                            for char in student.fiscal_code:
                                if char in nums:
                                    num_result += int(char)
                                else:
                                    characters = characters + char
                            num_result = int((num_result * num_result) + (num_result / 2))
                            char_result = characters[0] + characters[-1].lower() + characters[-3].lower() + characters[
                                4]
                            stringified_num = str(num_result)
                            if len(stringified_num) == 1:
                                stringified_num = stringified_num * 3
                            elif len(stringified_num) == 2:
                                stringified_num = stringified_num + stringified_num[:1]
                            char_result = char_result + stringified_num[0:3]
                            if num_result % 3 == 0:
                                char_result = char_result + '!'
                            elif num_result % 3 == 1:
                                char_result = char_result + '?'
                            else:
                                char_result = char_result + '@'

                            try:
                                user = User(username=student.fiscal_code,
                                            first_name=student.name,
                                            last_name=student.surname,
                                            )

                                user.set_password(char_result)
                                user.save()
                                students_group.user_set.add(user)
                                context['list'].append(
                                    f'{student.name} {student.surname}: Username {student.fiscal_code} - Password {char_result}')
                            except:
                                context[
                                    'error'] += f'{student.name} {student.surname}: Hai già creato questo account! ({student.fiscal_code} - {char_result} | '

                        else:
                            context['error'] += f'{student.name} {student.surname}: Codice fiscale non valido! | '

                    except:
                        context['error'] += f'{student.name} {student.surname}: Codice fiscale non presente! | '

                return render(request, 'create_student_user.html', context)
            else:
                return render(request, 'create_student_user.html', context)

        else:
            return render(request, 'create_student_user.html', context)
    else:
        return redirect('/')


def first_access_create_view(request):
    user_bound = request.GET.get('user_bound')
    error = ''
    for user in User.objects.all():
        if user.username == user_bound:
            user_bound = user
    if request.method == "POST":
        form = FirstAccessModelForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user = user_bound
            form.save()
            send_activation_mail(request, staff.user)
            return redirect("/")
        else:
            error = "Nel modulo sono presenti degli errori: " + str(sys.exc_info()[1])

    else:
        form = FirstAccessModelForm()
    context = {"form": form, 'error': error}
    return render(request, "staff/staff_create.html", context)


def handler500(request, exception=None, *_, **_k):
    if request.method == 'POST':
        send_bug_mail(request)
        return redirect('index')
    return render(request, "500.html", {
        "exception": exception
    })


def get_tutor_data():
    attendances = StudentAttendance.objects.all()
    students_n = len(Student.objects.all())
    previous_day = datetime.now().date() - timedelta(1)
    if attendances:
        absences = StudentAttendance.objects.filter(attendance_date=previous_day)
        counter = 1
        if len(absences.all()) <= 0:
            while len(absences.all()) <= 0:
                previous_day = previous_day - timedelta(1)
                absences = StudentAttendance.objects.filter(attendance_date=previous_day)
                counter += 1
                if counter == 7:
                    break
            absences = StudentAttendance.objects.filter(attendance_date=previous_day,
                                                        event__in=['A', 'S']).order_by('student__course')
        check_course = ''
        absences_dict = {}
        absences_n = 0
        for absence in absences:

            if absence.student.course.name != check_course:
                check_course = absence.student.course.name
                absences_dict[check_course] = ''
            absences_dict[check_course] += (str(absence.student) + " - ")
            absences_n += 1

        student_with_delays = Student.objects.filter(delays__gte=5).order_by('course__name', 'surname')
        check_course = ''
        delays_dict = {}
        student_with_delays_n = 0
        for delay in student_with_delays:

            if delay.course.name != check_course:
                check_course = delay.course.name
                delays_dict[check_course] = []
            delays_dict[check_course].append(delay)

            student_with_delays_n += 1
    else:
        delays_dict, absences_dict = {}, {}
        student_with_delays_n, absences_n = 0, 0


    notes = Note.objects.filter(solved=False).order_by('-created_at')
    tutor_data = {'delays': delays_dict,
                  'delays_n': student_with_delays_n,
                  'absences': absences_dict,
                  'absences_n': int((absences_n * 100) / students_n),
                  'attendances_date': previous_day,
                  'notes': notes,
                  'reminders': notes.filter(reminder=True, reminder_date__lte=datetime.now().date())
                  }
    return tutor_data


def get_secretary_data(message='', action=''):
    secretary_data = {}
    lessons = LessonWithDate.objects.all()
    previous_day = datetime.now().date() - timedelta(1)

    if lessons.filter(lesson_date__lte=previous_day):
        while True:
            selected_lessons = lessons.filter(lesson_date=previous_day).order_by('training_unit__course', 'hour')
            if selected_lessons:
                break
            else:
                previous_day = previous_day - timedelta(days=1)
        for lesson in selected_lessons:
            if lesson.check_if_validate():
                selected_lessons = selected_lessons.exclude(pk=lesson.pk)
        secretary_data = {'lessons': selected_lessons,
                          'lessons_date': previous_day,
                          'message': message,
                          'action': action,
                          }

    return secretary_data
