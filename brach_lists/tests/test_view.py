from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from unittest import skip

from brach_lists.views import home_page
from brach_lists.models import Item,DayActivityUserList
from brach_lists.forms import ItemForm,EMPTY_ITEM_ERROR

# Create your tests here.
class HomePageTest(TestCase):

    def test_打开首页并返回正确的html(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'brach_lists/home.html')
    
    def test_提交选择支行并登录POST之后重定向(self):
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.post('/',data={'brach_id':'ylxxkj'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/brach_lists/ylxxkj/')


class ListViewTest(TestCase):


    def test_用post方式写入非法空值(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        return self.client.post(f'/brach_lists/{list_.id}/',data={'text':''})
    
    
    def test_打开清单页并返回正确的template(self):
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.get('/brach_lists/ylxxkj/')
        self.assertTemplateUsed(response,'brach_lists/list.html')
    
    
    def test_显示所有的动态项(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        Item.objects.create(text='itemey1',list=list_)
        Item.objects.create(text='itemey2',list=list_)
        
        response=self.client.get('/brach_lists/ylxxkj/')
        
        self.assertContains(response,'itemey1')
        self.assertContains(response,'itemey2')
        


    def test_可以保存POST请求(self):
        other_branch=DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')
        correct_branch=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        self.client.post(f'/brach_lists/{correct_branch.id}/',
            data={'text':'新的动态一条'}
            )
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'新的动态一条')
        self.assertEqual(new_item.list,correct_branch)
        
    def test_重新定位到list_view(self):
        other_branch=DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')
        correct_branch=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.post(f'/brach_lists/{correct_branch.id}/',
            data={'text':'新的动态一条'}
            )
        self.assertRedirects(response,f'/brach_lists/{correct_branch.id}/')
    
    def test_可以解析到正确的模板(self):
        other_branch=DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')
        correct_branch=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.get(f'/brach_lists/{correct_branch.id}/')
        self.assertEqual(response.context['list'],correct_branch)
    
    def test_可以去掉最后的标点符号(self):
        correct_branch=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        response=self.client.post(f'/brach_lists/{correct_branch.id}/',data={'text':'新的动态，一条；'})
        self.assertEqual(Item.objects.first().text,'新的动态，一条')
        response=self.client.post(f'/brach_lists/{correct_branch.id}/',data={'text':'新的第二条；动态一条。'})
        self.assertEqual(Item.objects.last().text,'新的第二条；动态一条')


    def test_空值错误可以解析到正确的模板(self):
        response=self.test_用post方式写入非法空值()
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'brach_lists/list.html')
        
        
    def test_空值错误可以返回合适的错误(self):
        response=self.test_用post方式写入非法空值()
        expected_error="您不能输入空值！！"
        self.assertContains(response,expected_error)
    
    
    def test_空值不会被创建到数据库(self):
        self.test_用post方式写入非法空值()
        self.assertEqual(DayActivityUserList.objects.count(),1)
        self.assertEqual(Item.objects.count(),0)
        
    
    def test_详细页面可以使用form模块(self):
        response=self.test_用post方式写入非法空值()
        self.assertIsInstance(response.context['form'],ItemForm)
        self.assertContains(response,'name="text"')
        
    
    @skip
    def test_重复值可以显示错误信息到lists页面页面(self):
        list1=DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')
        item1=Item.objects.create(list=list1,text='textey')

        response=self.client.post(
            f'/brach_lists/{list1.id}/',
            data={'text':'textey'}
        )

        expected_error='您不能输入重复的待办事项'
        self.assertContains(response,expected_error)
        self.assertTemplateUsed(response,'brach_id/list.html')
        self.assertEqual(Item.objects.all().count(),1)

