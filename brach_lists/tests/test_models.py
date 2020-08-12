from django.test import TestCase
from django.core.exceptions import ValidationError

from brach_lists.models import Item,DayActivityUserList

# Create your tests here.

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

    def test_不能保存空白项目(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        item=Item(list=list_,text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    
    def test_get_absolute_url(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        self.assertEqual(list_.get_absolute_url(),f'/brach_lists/{list_.id}/')