from django import forms
from brach_lists.models import Item


EMPTY_ITEM_ERROR='你不能输入空白'
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
