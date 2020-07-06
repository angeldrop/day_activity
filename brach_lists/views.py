from django.shortcuts import render,redirect
from brach_lists.models import Item,DayActivityUserList
import datetime

# Create your views here.
def home_page(request):
    brach_lists=DayActivityUserList.objects.all()
    if request.method=="POST":
        brach_id=request.POST['brach_id']
        return redirect(f'/brach_lists/{brach_id}/')
    
    return render(request,'brach_lists/home.html',{'brach_lists':brach_lists})



def view_list(request,brach_id):
    list_=DayActivityUserList.objects.get(id=brach_id)
    items=Item.objects.filter(list=list_)
    days=Item.objects.filter(list=list_).distinct('activity_date').order_by('-activity_date')
    today=datetime.datetime.today().date()
    things=[]
    for day in days:
        things.append([day.activity_date,
            [i.text for i in items.filter(activity_date=day.activity_date).order_by('record_date_time')]
            ])
    return render(request,'brach_lists/list.html',{'list':list_,'days':days,'today':today,'items':items,'things':things,})


def add_item(request,brach_id):
    list_=DayActivityUserList.objects.get(id=brach_id)
    text_temp=request.POST['item_text']
    if text_temp[-1] in ['；','。','！',',','.']:
        text_temp=text_temp[:-1]
    Item.objects.create(text=text_temp,list=list_)
    return redirect(f'/brach_lists/{brach_id}/')
