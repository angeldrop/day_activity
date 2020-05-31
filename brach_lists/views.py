from django.shortcuts import render,redirect
from brach_lists.models import Item

# Create your views here.
def home_page(request):
    if request.method=="POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/brach_lists/the-only-list-in-the-world/')
    return render(request,'brach_lists/home.html')



def view_list(request):
    items=Item.objects.all()
    return render(request,'brach_lists/list.html',{'items':items})
