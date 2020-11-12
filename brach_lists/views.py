from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from brach_lists.models import Item,DayActivityUserList
from brach_lists.forms import ExistingListItemForm,ItemForm,EMPTY_ITEM_ERROR
import datetime

# Create your views here.
def home_page(request):
    brach_lists=DayActivityUserList.objects.all()
    if request.method=="POST":
        brach_id=request.POST['brach_id']
        list_=DayActivityUserList.objects.get(id=brach_id)
        return redirect(list_)
    
    return render(request,'brach_lists/home.html',{'brach_lists':brach_lists})



def view_list(request,brach_id):
    list_=DayActivityUserList.objects.get(id=brach_id)
    error=None
    items=Item.objects.filter(list=list_)
    days=Item.objects.filter(list=list_).distinct('activity_date').order_by('-activity_date')
    today=datetime.datetime.today().date()
    things=[]
    for day in days:
        things.append([day.activity_date,
            [i.text for i in items.filter(activity_date=day.activity_date).order_by('record_date_time')]
            ])
    if request.method=='POST':
        text_temp=request.POST['text']
        if not len(text_temp)==0:
            if text_temp[-1] in ['；','。','！',',','.']:
                text_temp=text_temp[:-1]
        form=ExistingListItemForm(for_list=list_,data={'text':text_temp})
        if form.is_valid():
            form.save()
            # Item.objects.create(text=text_temp,list=list_)
            return redirect(list_)
    else:
        form=ExistingListItemForm(for_list=list_)    
    return render(request,'brach_lists/list.html',{'list':list_,'days':days,'today':today,'items':items,'things':things,'error':error,'form':form})

