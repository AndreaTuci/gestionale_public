from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Classroom, Company, Convention, Course, CourseType, DisciplinaryMeasure, Stage, Sector

from .forms import ClassroomModelForm, CommunicationCourseModelForm, CompanyModelForm, ConventionModelForm, \
    CourseModelForm, CourseTypeModelForm, \
    DisciplinaryMeasureModelForm, SectorModelForm, CreateStaffModelForm, UpdateStaffModelForm, StudentModelForm, \
    TrainingUnitModelForm, UpdateAdminStaffModelForm, CompanyUpdateModelForm, ConventionUpdateModelForm, \
    CourseUpdateModelForm, DisciplinaryMeasureUpdateModelForm, StageModelForm, StageUpdateModelForm, \
    StudentUpdateModelForm

from frequenze.models import FamilyCommunication
from amministrazione.models import TeacherAgreement
from .utils import csv_reader, csv_reader_student_list, set_permissions, copy_spreadsheet, csv_regione_toscana_reader
from .serializers import *
from frequenze.models import *
import sys
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from openpyxl import load_workbook
from core.auth_lists import BACKOFFICE
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        student = Student.objects.get(fiscal_code=user)
        course = Course.objects.get(pk=student.course.pk)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'course': course.pk
        })

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class StudentAPIListView(generics.ListCreateAPIView):
    """
    API endpoint
    """

    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Student.objects.filter(fiscal_code=self.request.user)
        return queryset


class StudentAPIDetailView(generics.RetrieveAPIView):
    """
    API endpoint
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'fiscal_code'

    def get_queryset(self):
        queryset = Student.objects.filter(fiscal_code=self.request.user)
        return queryset


class DisciplinaryMeasureAPIDetailView(generics.ListAPIView):
    """
    API endpoint
    """
    serializer_class = DisciplinaryMeasureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        fiscal_code = self.kwargs['fiscal_code']
        return DisciplinaryMeasure.objects.filter(students__fiscal_code=fiscal_code).order_by("-reporting_date")


class DisciplinaryMeasureAPIUpdateView(generics.RetrieveUpdateAPIView):
    """
    API endpoint
    """
    serializer_class = DisciplinaryMeasureUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        measure = str(self.kwargs['measure_id'])
        student = self.request.user.username
        try:
            return DisciplinaryMeasureRead.objects.get(measure__iexact=measure,
                                                       student__iexact=student)

        except:
            return


class CommunicationAPIListView(generics.ListCreateAPIView):
    serializer_class = CommunicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Communication.objects.filter(student__fiscal_code=self.request.user)
        return queryset


class CommunicationAPIUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CommunicationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Communication.objects.all()


########################################################################################################################

def communication_course_detail(request, course, pk):
    permission = request.user.has_perm('anagrafica.view_communication')
    if permission:
        course = get_object_or_404(Course, pk=course)
        communication = get_object_or_404(Communication, pk=pk)
        context = {"course": course, "communication": communication}
        return render(request, "communication/communication_course_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


def communication_student_list(request, student):
    permission = request.user.has_perm('anagrafica.view_communication')
    if permission:
        student = get_object_or_404(Student, pk=student)
        communications = Communication.objects.filter(student=student).order_by('-created_at')
        context = {"student": student, "communications": communications}
        return render(request, "communication/communication_student_list.html", context)
    else:
        return render(request, 'missing_auth.html')


def single_communication_detail(request, pk):
    permission = request.user.has_perm('anagrafica.view_communication')
    if permission:
        communication = get_object_or_404(Communication, pk=pk)
        context = {"communication": communication}
        return render(request, "communication/single_communication_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


def single_communication_create(request, student):
    permission = request.user.has_perm('anagrafica.add_communication')
    if permission:
        student = get_object_or_404(Student, pk=student)
        if request.method == 'POST':
            form = CommunicationCourseModelForm(data=request.POST)
            if form.is_valid():
                communication = Communication(student=student,
                                              subject=form.cleaned_data['subject'],
                                              content=form.cleaned_data['content'],
                                              created_at=form.cleaned_data['created_at'])
                communication.save()
                comm_id = communication.pk
                return redirect('single-communication-detail', pk=comm_id)
            else:
                return render(request, "communication/single_communication_create.html",
                              {"form": form, 'student': student})
        else:
            form = CommunicationCourseModelForm()
            return render(request, "communication/single_communication_create.html", {"form": form, "student": student})
    else:
        return render(request, 'missing_auth.html')


def communication_create_course(request, course):
    permission = request.user.has_perm('anagrafica.add_communication')
    if permission:
        course = get_object_or_404(Course, pk=course)
        if request.method == 'POST':
            form = CommunicationCourseModelForm(data=request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                content = form.cleaned_data['content']
                created_at = form.cleaned_data['created_at']
                comm_id = 0
                for student in Student.objects.filter(course=course):
                    communication = Communication(student=student,
                                                  subject=subject,
                                                  content=content,
                                                  created_at=created_at)
                    communication.save()
                    comm_id = communication.pk

                return redirect('communication-course-detail', course=course.pk, pk=comm_id)
            else:
                return render(request, "communication/communication_course_create.html",
                              {"form": form, "course": course})
        else:
            form = CommunicationCourseModelForm()
            return render(request, "communication/communication_course_create.html", {"form": form, "course": course})
    else:
        return render(request, 'missing_auth.html')


class ClassroomListView(PermissionRequiredMixin,
                        ListView):
    permission_required = 'anagrafica.view_classroom'
    queryset = Classroom.objects.all().order_by("name")
    paginate_by = 25
    template_name = 'classroom/classroom_list.html'
    context_object_name = "list"


class ClassroomCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_classroom'
    model = Classroom
    form_class = ClassroomModelForm
    template_name = "classroom/classroom_create.html"
    success_url = "/"


def classroom_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_classroom')
    if permission:
        classroom = get_object_or_404(Classroom, pk=pk)
        context = {"classroom": classroom}
        return render(request, "classroom/classroom_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class ClassroomUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_classroom'
    model = Classroom
    form_class = ClassroomModelForm
    template_name_suffix = "_update_form"


class ClassroomDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_classroom'
    model = Classroom
    template_name = "classroom/classroom_confirm_delete.html"
    success_url = "classroom/classroom_list.html"


########################################################################################################################


class CompanyListView(PermissionRequiredMixin,
                      ListView):
    permission_required = 'anagrafica.view_company'
    queryset = Company.objects.all().order_by("sector", "operational_headquarters_city", "name")
    paginate_by = 100
    template_name = 'company/company_list.html'
    context_object_name = "company_list"


def companies_add(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            error = ''
            try:
                spreadsheet = request.FILES['file'].file
                sector = request.POST.get('sector')
                copy_error = copy_spreadsheet(spreadsheet, sector)
            except BaseException:
                error = "Errore: " + str(sys.exc_info()[1])
            return render(request, 'company/companies_added.html', context={'error': error, 'copy_error': copy_error})

    return render(request, 'company/companies_added.html')


class CompanyCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_company'
    model = Company
    form_class = CompanyModelForm
    template_name = "company/company_create.html"
    success_url = "/"


def company_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_company')
    if permission:
        company = get_object_or_404(Company, pk=pk)
        context = {"company": company}
        return render(request, "company/company_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class CompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_company'
    model = Company
    form_class = CompanyUpdateModelForm
    template_name = "company/company_update.html"

    def get_success_url(self):
        return reverse('company-list')


class CompanyDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_company'
    model = Company
    template_name = "company/company_confirm_delete.html"
    success_url = "company/company_list.html"


########################################################################################################################


class ConventionListView(PermissionRequiredMixin,
                         ListView):
    permission_required = 'anagrafica.view_convention'
    queryset = Convention.objects.all().order_by("-date")
    paginate_by = 25
    template_name = 'convention/convention_list.html'
    context_object_name = "list"


class ConventionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_convention'
    model = Convention
    form_class = ConventionModelForm
    template_name = "convention/convention_create.html"
    success_url = "/"


def convention_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_convention')
    if permission:
        convention = get_object_or_404(Convention, pk=pk)
        context = {"convention": convention}
        return render(request, "convention/convention_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class ConventionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_convention'
    model = Convention
    form_class = ConventionUpdateModelForm
    template_name_suffix = "_update_form"


class ConventionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_convention'
    model = Convention
    template_name = "convention/convention_confirm_delete.html"
    success_url = "convention/convention_list.html"


########################################################################################################################


class CourseListView(PermissionRequiredMixin,
                     ListView):
    permission_required = 'anagrafica.view_course'
    queryset = Course.objects.filter(is_finished=False).order_by("name")
    paginate_by = 25
    template_name = 'course/course_list.html'
    context_object_name = "list"

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = Course.objects.filter(is_finished=False).order_by("name")
        attendances = {}
        for course in queryset:
            course.todays_attendances_exists()
            students = course.get_students()
            try:
                StudentAttendance.objects.filter(attendance_date=datetime.now, student__in=students)
                attendances[course] = 1
            except:
                attendances[course] = 0
        return {'queryset': queryset, 'attendances': attendances, 'backoffice': BACKOFFICE}


class CourseCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_course'
    model = Course
    form_class = CourseModelForm
    template_name = "course/course_create.html"
    success_url = "/"


def course_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_course')

    if permission:
        course = get_object_or_404(Course, pk=pk)
        date = datetime.now().date()
        year = datetime.strftime(datetime.now(), '%Y')
        month = datetime.strftime(datetime.now(), '%m')
        students = Student.objects.filter(course=course).order_by('number', 'surname', 'name')
        try:
            family_communications = FamilyCommunication.objects.get(year=year, month=month, course=course)
        except BaseException:
            family_communications = FamilyCommunication.objects.create(year=year, month=month, course=course, text='')
        context = {"course": course,
                   "date": date,
                   "students": students,
                   "year": year,
                   "month": month,
                   "communications": family_communications,
                   "backoffice": BACKOFFICE,
                   }

        # if request.method == 'POST':
        #    print(request.POST.get('text'))
        #    family_communications.text = request.POST.get('text')
        #    family_communications.save()

        return render(request, "course/course_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


def course_detail_inail_view(request, pk):
    permission = request.user.profile.get_task_display() in BACKOFFICE

    if permission:
        course = get_object_or_404(Course, pk=pk)
        students = Student.objects.filter(course_id=pk, is_withdrawn=False).order_by('number')
        context = {"course": course,
                   "students": students,
                   "backoffice": BACKOFFICE,
                   }

        return render(request, "course/course_detail_inail.html", context)
    else:
        return render(request, 'missing_auth.html')


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_course'
    model = Course
    form_class = CourseUpdateModelForm
    template_name_suffix = "_update_form"


class CourseDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_course'
    model = Course
    template_name = "course/course_confirm_delete.html"
    success_url = "course/course_list.html"


########################################################################################################################


class CourseTypeListView(PermissionRequiredMixin,
                         ListView):
    permission_required = 'anagrafica.view_coursetype'
    queryset = CourseType.objects.all().order_by("course_type")
    paginate_by = 25
    template_name = 'course-type/coursetype_list.html'
    context_object_name = "list"


class CourseTypeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_coursetype'
    model = CourseType
    form_class = CourseTypeModelForm
    template_name = "course-type/coursetype_create.html"
    success_url = "/"


def course_type_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_coursetype')
    if permission:
        coursetype = get_object_or_404(CourseType, pk=pk)
        context = {"coursetype": coursetype}
        return render(request, "course-type/coursetype_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class CourseTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_coursetype'
    model = CourseType
    form_class = CourseTypeModelForm
    template_name_suffix = "_update_form"


class CourseTypeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_coursetype'
    model = CourseType
    template_name = "course-type/coursetype_confirm_delete.html"
    success_url = "course-type/coursetype_list.html"


########################################################################################################################


class DisciplinaryMeasureListView(PermissionRequiredMixin,
                                  ListView):
    permission_required = 'anagrafica.view_disciplinarymeasure'
    queryset = DisciplinaryMeasure.objects.all().order_by("-reporting_date")
    paginate_by = 25
    template_name = 'disciplinary-measure/disciplinarymeasure_list.html'
    context_object_name = "list"


class DisciplinaryMeasureListByStudentView(PermissionRequiredMixin,
                                           ListView):
    permission_required = 'anagrafica.view_disciplinarymeasure'
    paginate_by = 25
    template_name = 'disciplinary-measure/disciplinarymeasure_list.html'

    def get_queryset(self):
        queryset = DisciplinaryMeasure.objects.filter(students__pk__icontains=self.kwargs['student']).order_by(
            "-reporting_date")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = DisciplinaryMeasure.objects.filter(students__pk=self.kwargs['student']).order_by(
            "-reporting_date")
        student = Student.objects.get(pk=self.kwargs['student'])
        return {'student': student, 'list': queryset}


class DisciplinaryMeasureCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_disciplinarymeasure'
    model = DisciplinaryMeasure
    form_class = DisciplinaryMeasureModelForm
    template_name = "disciplinary-measure/disciplinarymeasure_create.html"
    success_url = "/"


class DisciplinaryMeasureCourseCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_disciplinarymeasure'
    model = DisciplinaryMeasure
    form_class = DisciplinaryMeasureModelForm
    template_name = "disciplinary-measure/disciplinarymeasure_create.html"
    success_url = "/"

    def get_form(self, form_class=None):
        form = super(DisciplinaryMeasureCourseCreateView, self).get_form(form_class)  # instantiate using parent
        form.fields['students'].queryset = Student.objects.filter(course=self.kwargs['course'], is_withdrawn=False)
        form.fields['students'].label = 'Allievi* [CTRL + Click per selezionare più allievi]'
        return form


def disciplinary_measure_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_disciplinarymeasure')
    if permission:
        disciplinarymeasure = get_object_or_404(DisciplinaryMeasure, pk=pk)
        context = {"disciplinarymeasure": disciplinarymeasure}
        return render(request, "disciplinary-measure/disciplinarymeasure_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class DisciplinaryMeasureUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_disciplinarymeasure'
    model = DisciplinaryMeasure
    form_class = DisciplinaryMeasureUpdateModelForm
    template_name = "disciplinary-measure/disciplinarymeasure_update.html"

    def get_success_url(self):
        return reverse('course-list')


class DisciplinaryMeasureDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_disciplinarymeasure'
    model = DisciplinaryMeasure
    template_name = "disciplinary-measure/disciplinarymeasure_confirm_delete.html"
    success_url = "disciplinary-measure/disciplinarymeasure_list.html"


########################################################################################################################


class SectorListView(PermissionRequiredMixin,
                     ListView):
    permission_required = 'anagrafica.view_sector'
    queryset = Sector.objects.all().order_by("sector_name")
    paginate_by = 25
    template_name = 'sector/sector_list.html'
    context_object_name = "list"


class SectorCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_sector'
    model = Sector
    form_class = SectorModelForm
    template_name = "sector/sector_create.html"
    success_url = "/"


def sector_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_sector')
    if permission:
        sector = get_object_or_404(Sector, pk=pk)
        context = {"sector": sector}
        return render(request, "sector/sector_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class SectorUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_sector'
    model = Sector
    form_class = SectorModelForm
    template_name_suffix = "_update_form"


class SectorDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_sector'
    model = Sector
    template_name = "sector/sector_confirm_delete.html"
    success_url = "sector/sector_list.html"


########################################################################################################################


class StaffListView(PermissionRequiredMixin,
                    ListView):
    permission_required = 'anagrafica.view_staff'
    queryset = Staff.objects.all().order_by("surname")
    paginate_by = 100
    template_name = 'staff/staff_list.html'
    context_object_name = "list"


class StaffCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_staff'
    model = Staff
    form_class = CreateStaffModelForm
    template_name = "staff/staff_create.html"
    success_url = "/"


def staff_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_sector')
    if permission:
        context = {}
        staff = get_object_or_404(Staff, pk=pk)
        # spec = user.profile.specialization.all()
        if request.user.profile.pk == staff.pk or request.user.is_superuser or request.user.profile.task in ['S', 'C', 'P']:
            context["profile"] = staff
            # context['specialization'] = spec
        else:
            context["profile"] = "invalid_profile"
        return render(request, "staff/staff_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class StaffUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_staff'
    model = Staff
    form_class = UpdateStaffModelForm
    template_name = "staff/staff_update.html"

    def get_success_url(self):
        pk = self.request.user.profile.pk
        return reverse('staff-detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = {}
        user = get_object_or_404(User, pk=self.request.user.pk)
        if self.kwargs['pk'] == user.profile.pk:
            context = super().get_context_data(**kwargs)
            context['object'] = user
            context["profile"] = user
        else:
            context["profile"] = "invalid_profile"
        return context


@user_passes_test(lambda u: u.is_superuser)
def staff_activate_view(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.active = True
        staff.save()
        return redirect('index')
    else:

        return render(request, "staff/staff_activate.html",
                      {"staff": staff})


class StaffAdminUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.delete_staff'
    model = Staff
    form_class = UpdateAdminStaffModelForm
    template_name = "staff/staff_update.html"
    success_url = '/'

    def form_valid(self, form):
        task = form.cleaned_data['task']
        user = User.objects.get(profile=self.kwargs['pk'])
        set_permissions(user, task)
        return super(StaffAdminUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        user = Staff.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['profile'] = user

        return context


class StaffDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_staff'
    model = Staff
    template_name = "staff/staff_confirm_delete.html"
    success_url = "staff/staff_list.html"


########################################################################################################################


class StageListView(PermissionRequiredMixin,
                    ListView):
    permission_required = 'anagrafica.view_stage'
    queryset = Stage.objects.all().order_by("-end_date", "course")
    paginate_by = 100
    template_name = 'stage/stage_list.html'
    context_object_name = "list"


class StageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_stage'
    model = Stage
    form_class = StageModelForm
    template_name = "stage/stage_create.html"
    success_url = "/"


def stage_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_stage')
    if permission:
        stage = get_object_or_404(Stage, pk=pk)
        students = Student.objects.filter(course=stage.course)
        context = {"stage": stage, 'students': students}
        return render(request, "stage/stage_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


def stage_convention_detail_view(request, stage, student):
    permission = request.user.has_perm('anagrafica.view_stage')
    if permission:
        stage_obj = get_object_or_404(Stage, pk=stage)
        student_obj = get_object_or_404(Student, pk=student)
        context = {"stage": stage_obj, 'student': student_obj}
        return render(request, "stage/stage_convention_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class StageUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_stage'
    model = Stage
    form_class = StageUpdateModelForm
    template_name = "stage/stage_update.html"

    def get_success_url(self):
        return reverse('course-detail', args=[self.request.POST.get('course')])


class StageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_stage'
    model = Stage
    template_name = "stage/stage_confirm_delete.html"
    success_url = "/"


########################################################################################################################


class StudentListView(PermissionRequiredMixin,
                      ListView):
    permission_required = 'anagrafica.view_student'
    queryset = Student.objects.all().order_by("surname")
    paginate_by = 25
    template_name = 'student/student_list.html'
    context_object_name = "list"


class StudentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_student'
    model = Student
    form_class = StudentModelForm
    template_name = "student/student_create.html"
    success_url = "/"


def student_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_student')
    if permission:
        student = get_object_or_404(Student, pk=pk)
        address = student.resident_in_address.replace(' ', '+')
        companies = f'https://www.google.com/maps/search/?api=1&query={address}+{student.resident_in_city}+{student.course.sector.sector_name}&zoom=20'
        context = {"student": student, 'companies': companies}
        return render(request, "student/student_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class StudentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_student'
    model = Student
    form_class = StudentUpdateModelForm
    template_name = "student/student_update.html"

    def get_success_url(self):
        return reverse('course-detail', args=[self.request.POST.get('course')])


class StudentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_student'
    model = Student
    template_name = "student/student_confirm_delete.html"
    success_url = "/"


########################################################################################################################


class TeacherListView(PermissionRequiredMixin,
                      ListView):
    permission_required = 'anagrafica.view_staff'
    queryset = Staff.objects.filter(task="D").order_by("surname")
    template_name = 'teacher/teacher_list.html'
    context_object_name = "teacher_list"

    def get_context_data(self, **kwargs):
        teachers = Staff.objects.filter(task="D").order_by('reference_teacher__training_unit', "surname")
        backoffice = Staff.objects.exclude(task="D").order_by('task', "surname")
        return {'backoffice': backoffice,
                'teacher_list': teachers}
        # context = super(TeacherListView, self).get_context_data(**kwargs)
        # teachers = context['teacher_list']
        # for teacher in teachers:
        #    context[teacher] = teacher.specialization.all()
        # context['specialization_list'] = Sector.objects.all()
        # return context


########################################################################################################################


class TrainingUnitListView(PermissionRequiredMixin,
                           ListView):
    permission_required = 'anagrafica.view_trainingunit'
    queryset = TrainingUnit.objects.filter(course__is_finished=False).order_by("course", "code")
    template_name = 'training-unit/trainingunit_list.html'
    context_object_name = "list"


class TrainingUnitCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'anagrafica.add_trainingunit'
    model = TrainingUnit
    form_class = TrainingUnitModelForm
    template_name = "training-unit/trainingunit_create.html"

    def get_success_url(self):
        return reverse('trainingunit-list')


def training_unit_detail_view(request, pk):
    permission = request.user.has_perm('anagrafica.view_trainingunit')
    if permission:
        trainingunit = get_object_or_404(TrainingUnit, pk=pk)
        units_in_course = TrainingUnit.objects.filter(course=trainingunit.course).order_by("code")
        context = {"trainingunit": trainingunit, "units_in_course": units_in_course}
        return render(request, "training-unit/trainingunit_detail.html", context)
    else:
        return render(request, 'missing_auth.html')


class TrainingUnitUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'anagrafica.change_trainingunit'
    model = TrainingUnit
    form_class = TrainingUnitModelForm
    template_name = "training-unit/trainingunit_create.html"

    def get_success_url(self):
        return reverse('trainingunit-list')


class TrainingUnitDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'anagrafica.delete_trainingunit'
    model = TrainingUnit
    template_name = "training-unit/trainingunit_confirm_delete.html"
    success_url = "training-unit/trainingunit_list.html"


########################################################################################################################

@login_required
def upload_csv(request):
    csv_content = []
    error = ''
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file'].file
            csv_content = csv_reader(csv_file)
        except BaseException:
            error = "Il file caricato non corrisponde ai criteri: " + str(sys.exc_info()[1])

    return render(request, 'student/student_log_upload.html', {'content': csv_content, 'error': error})


@login_required
def upload_csv_regione_toscana(request):
    csv_content = []
    error = ''
    courses = Course.objects.all().order_by('name')
    if request.method == 'POST':
        try:
            course_pk = request.POST.get('search_course')
            course = Course.objects.get(pk=course_pk)
            csv_file = request.FILES['file'].file
            csv_content = csv_regione_toscana_reader(csv_file, course)
        except BaseException:
            error = "Il file caricato non corrisponde ai criteri: " + str(sys.exc_info()[1])

    return render(request, 'student/upload_students_in_course.html', {'content': csv_content,
                                                                      'courses': courses,
                                                                      'error': error})


@login_required
def upload_students_csv(request):
    csv_content = []
    error = ''
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file'].file
            csv_content = csv_reader_student_list(csv_file)
        except BaseException:
            error = "Il file caricato non corrisponde ai criteri: " + str(sys.exc_info()[1])

    return render(request, 'student/student_upload.html', {'content': csv_content, 'error': error})
