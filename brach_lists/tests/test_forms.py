from django.test import TestCase


from brach_lists.forms import ItemForm,EMPTY_ITEM_ERROR

# Create your tests here.

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