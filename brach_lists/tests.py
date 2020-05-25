from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from brach_lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并解析到指定view下函数(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_首页返回正确的html(self):
        request=HttpRequest()
        response=home_page(request)
        html=response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>榆林分行报动态系统</title>',html)
        self.assertTrue(html.endswith('</html>'))