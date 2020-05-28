from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from brach_lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并返回正确的html(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'brach_lists/home.html')
    
    def test_可以保存POST请求(self):
         response=self.client.post('/',data={'item_text':'新的动态一条'})
         self.assertIn('新的动态一条',response.content.decode())
         self.assertTemplateUsed(response,'brach_lists/home.html')