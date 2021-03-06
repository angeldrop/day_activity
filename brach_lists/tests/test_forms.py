from django.test import TestCase

from brach_lists.models import Item,DayActivityUserList
from brach_lists.forms import (
    ItemForm,ExistingListItemForm,
    EMPTY_ITEM_ERROR,DUPLICATE_ITEM_ERROR
)

# Create your tests here.

class ExistingListItemFormTest(TestCase):
    def test_form渲染item_text的input(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        form=ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="请输入动态事项"',form.as_p())
        

    def test_form输入空值验证(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        form=ExistingListItemForm(for_list=list_,data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )


    def test_form重复值验证数据(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        Item.objects.create(list=list_,text='no twins!')
        form=ExistingListItemForm(for_list=list_,data={'text':'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_ITEM_ERROR]
        )


class ItemFormTest(TestCase):

    def test_form渲染placeholder和css的classes(self):
        form=ItemForm()
        self.assertIn('placeholder="请输入动态事项"',form.as_p())
        self.assertIn('class="form-control form-control-lg"',form.as_p())
    
    
    def test_form输入空值验证(self):
        form=ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )
        
        
    def test_form保存数据(self):
        list_=DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        form=ItemForm(data={'text':'god，help us.'})
        new_item=form.save(for_list=list_)
        self.assertEqual(new_item,Item.objects.first())
        self.assertEqual(new_item.text,'god，help us.')
        self.assertEqual(new_item.list,list_)