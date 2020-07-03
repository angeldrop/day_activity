from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from brach_lists.views import home_page
from brach_lists.models import Item,DayActivityUserList

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并返回正确的html(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'brach_lists/home.html')
    
    def test_提交选择支行并登录POST之后重定向(self):
        response=self.client.post('/',data={'brach_id':'ylxxkj'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/brach_lists/ylxxkj/')


class ItemModelTest(TestCase):
    def test_保存并提取Item数据库项目(self):
        list_ = DayActivityUserList.objects.create()
        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.list=list_
        first_item.save()
        
        second_item=Item()
        second_item.text='Item the second'
        second_item.list=list_
        second_item.save()
        
        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_saved_item.text,'Item the second')
    def test_保存并提取DayActivityUserList数据库项目(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        saved_userlist=DayActivityUserList.objects.all()
        self.assertEqual(saved_userlist.count(),1)
        self.assertEqual(saved_userlist[0].full_name,'信息科技部')


class ListViewTest(TestCase):
    def test_打开清单页并返回正确的template(self):
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.get('/brach_lists/ylxxkj/')
        self.assertTemplateUsed(response,'brach_lists/list.html')
    
    def test_可以保存POST请求(self):
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.post('/brach_lists/ylxxkj/',data={'item_text':'新的动态一条'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'新的动态一条')
    
    def test_显示所有的动态项(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        Item.objects.create(text='itemey1',list=list_)
        Item.objects.create(text='itemey2',list=list_)
        
        response=self.client.get('/brach_lists/ylxxkj/')
        
        self.assertContains(response,'itemey1')
        self.assertContains(response,'itemey2')
        
    def test_可以去掉最后的标点符号(self):
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.post('/brach_lists/ylxxkj/',data={'item_text':'新的动态，一条；'})
        self.assertEqual(Item.objects.first().text,'新的动态，一条')
        response=self.client.post('/brach_lists/ylxxkj/',data={'item_text':'新的第二条；动态一条。'})
        self.assertEqual(Item.objects.last().text,'新的第二条；动态一条')