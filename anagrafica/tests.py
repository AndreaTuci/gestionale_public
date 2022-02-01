from django.test import TestCase
from .models import *
import datetime

class CourseModelValidationTest(TestCase):
    def test_setUp(self):
        course_type = CourseType.objects.create(course_type="IeFP")
        sector = Sector.objects.create(sector_name="Elettricisti")
        course = Course.objects.create(type=course_type,
                              sector=sector,
                              name="ELE",
                              start_date="2020-01-01",
                              expected_end_date="2022-01-01",
                              actual_end_date="2022-03-01",
                              duration=2800,
                              classroom_h=1400,
                              stage_h=1400
                              )

        course.clean()

