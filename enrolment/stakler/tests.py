from django.test import TestCase
from stakler.models import Teacher


class TeacherTestCase(TestCase):
    def setUp(self):
        Teacher.objects.create(id=0, first_name='Tomasz', last_name='Testowy')


    def test_creation(self):
        t = Teacher.objects.get(id=0)
        self.assertEqual(t.first_name, 'Tomasz')
        self.assertEqual(t.last_name, 'Testowy')
