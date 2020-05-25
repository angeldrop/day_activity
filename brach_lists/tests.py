from django.test import TestCase
from django.urls import resolve
from brach_lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并解析(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)