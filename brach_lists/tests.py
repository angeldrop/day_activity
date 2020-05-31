from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from brach_lists.views import home_page
from brach_lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并返回正确的html(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'brach_lists/home.html')
    
    def test_可以保存POST请求(self):
        response=self.client.post('/',data={'item_text':'新的动态一条'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'新的动态一条')

    def test_POST之后重定向(self):
        response=self.client.post('/',data={'item_text':'新的动态一条'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/brach_lists/the-only-list-in-the-world/')

    def test_在必要的时候才保存item(self):
        response=self.client.get('/')
        self.assertEqual(Item.objects.count(),0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.save()
        
        second_item=Item()
        second_item.text='Item the second'
        second_item.save()
        
        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_saved_item.text,'Item the second')


class ListViewTest(TestCase):
    def test_打开q清单页并返回正确的template(self):
        response=self.client.get('/brach_lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'brach_lists/list.html')
    
    
    def test_显示所有的动态项(self):
        Item.objects.create(text='itemey1')
        Item.objects.create(text='itemey2')
        
        response=self.client.get('/brach_lists/the-only-list-in-the-world/')
        
        self.assertContains(response,'itemey1')
        self.assertContains(response,'itemey2')