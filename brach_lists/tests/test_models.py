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
    
    
    def test_不能重复项目(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        Item.objects.create(list=list_,text='bla')
        with self.assertRaises(ValidationError):
            item=Item(list=list_,text='bla')
            item.full_clean()
    
    
    def test_不能过度限制重复项目(self):
        list1 = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        list2 = DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')
        Item.objects.create(list=list1,text='bla')
        item=Item(list=list2,text='bla')
        item.full_clean()    #不该抛出异常
    
    
    def test_item默认文本为空白(self):
        item=Item()
        self.assertEqual(item.text,'')
        
        
    def test_item和DayActivityUserList关联(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        item=Item()
        item.list=list_
        item.save()
        self.assertIn(item,list_.item_set.all())
    
class DayActivityUserListModelTest(TestCase):    
    def test_get_absolute_url(self):
        list_ = DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        self.assertEqual(list_.get_absolute_url(),f'/brach_lists/{list_.id}/')