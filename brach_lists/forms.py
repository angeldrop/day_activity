from django import forms
from brach_lists.models import Item
from django.core.exceptions import ValidationError


EMPTY_ITEM_ERROR='您不能输入空值！！'
DUPLICATE_ITEM_ERROR='您不能输入重复的待办事项'
# Create your forms here.

class ItemForm(forms.models.ModelForm):
    
    class Meta:
        model=Item
        fields=('text',)
        widgets={
            'text':forms.fields.TextInput(attrs={
                'placeholder':"请输入动态事项",
                'class':"form-control form-control-lg",
            }),
        }
        error_messages={
            'text':{'required':EMPTY_ITEM_ERROR}
        }
    def save(self,for_list):
        self.instance.list=for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    def __init__(self,for_list,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.list=for_list
        
    
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict={'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
