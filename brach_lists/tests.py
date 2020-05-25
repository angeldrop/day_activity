from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from brach_lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并返回正确的html(self):
        response=self.client.get('/')

        self.assertTemplateUsed(response,'brach_lists/home.html')
        