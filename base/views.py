from django.shortcuts import render,redirect
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from .forms import RoomForm,Userform,MyUserCreationForm

# rooms=[
#       {'id':1,"name":"lets learn python"},
#       {'id':2,"name":"design with me "},
#       {'id':3,"name":"frontend devlopers"},
# ]

def home(request):
  q=request.GET.get("q") if request.GET.get("q")!=None else ""
  rooms= Room.objects.filter(Q(topic__name__contains=q) |
  Q(name__contains=q)  |
  Q(description__contains=q)                              
  )
  count_room=rooms.count()
  topics=Topic.objects.all()[0:5]
  room_messages=Message.objects.filter(Q(room__topic__name__contains=q))

  context={'rooms':rooms,'topics':topics,"count":count_room,"room_messages":room_messages}  
  return render(request,'base/home.html',context)

def Profile(request,pk):
  user=User.objects.get(id=pk)
  rooms=user.room_set.all()
  room_messages=user.message_set.all()
  topics=Topic.objects.all()
  context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
  return render(request,'base/profile.html',context)




def room(request,pk):
  room=Room.objects.get(id=pk )
  room_messages=room.message_set.all().order_by("-created")
  participants=room.participants.all()
  if request.method=="POST":
    message=Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get("body")
    )
    room.participants.add(request.user)
    return redirect('room',pk=room.id)

  # room = None
  # for i in rooms:
  #   if i['id']== int(pk):
  #     room=i
  context={'room':room,'room_messages':room_messages,"participants":participants}   
  return render(request,"base/room.html",context)
@login_required(login_url="login")
def Create(request):
  form=RoomForm()
  topics=Topic.objects.all()
  if request.method=="POST":
    topic_name=request.POST.get('topic')
    topic,created=Topic.objects.get_or_create(name=topic_name)
    Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('name'),
      description=request.POST.get('description'),
    )
    return redirect("/")
  context={"form":form,"topics":topics}
  return render(request,"base/create.html",context)
@login_required(login_url="login")
def Update(request,pk):
  room=Room.objects.get(id=pk)
  form=RoomForm(instance=room)
  topics=Topic.objects.all()
  if request.user!=room.host:
    return HttpResponse("you are not allowed here")
  if request.method=="POST":
    form=RoomForm(request.POST,instance=room)
    if form.is_valid():
      form.save()
      return redirect("/")


  context={"form":form,"topics":topics,"room":room}
  return render(request,"base/create.html",context)

@login_required(login_url="login")
def Delete(request,pk):
  room=Room.objects.get(id=pk)
  context={"obj":room}
  if request.user!=room.host:
    return HttpResponse("you are not allowed here")
  if request.method=="POST":
    room.delete()
    return redirect("/")
  return render(request,'base/delete.html',context)

def Login_user(request):
  page = 'login'
  loginform=Userform()
  if request.user.is_authenticated:
    return redirect("/")
  if request.method=="POST":
    name=request.POST["username"].lower()
    password=request.POST["password"]
    try:
      user=User.objects.get(username=name)
    except:
      messages.error(request, "User does not Exist")
    user=authenticate(request,username=name,password=password)
    if user is not None:
      login(request,user)
      return redirect('/')  
    else:
      messages.error(request,"username or pass does not exist")

  context={"page":page,"loginform":loginform}
  return render(request,'base/user_login.html',context)
def Register_user(request):
  page='register'
  form=MyUserCreationForm()
  if request.method=="POST":
    form=MyUserCreationForm(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.username=user.username.lower()
      user.save()
      login(request,user)
      return redirect("/")
    else:
      messages.error(request,"An error occured during registraion")
  return render(request,'base/user_login.html',{"form":form})
def Logut_user(request):
  logout(request)
  return redirect('/')

@login_required(login_url="login")
def DeleteMessage(request,pk):
  message=Message.objects.get(id=pk)

  if request.user!=message.user:
    return HttpResponse("you are not allowed here")
  if request.method=="POST":
    message.delete()
    return redirect("/")
  context={"obj":message}
  return render(request,'base/delete.html',context)

@login_required(login_url="login")
def updateUser(request):
  user=request.user
  form=Userform(instance=user)
  if request.method=="POST":
    form=Userform(request.POST,request.FILES,instance=user)
    if form.is_valid():
      form.save()
      return redirect('profile',pk=user.id)
  context={'form':form}
  return render(request,'base/update_user.html',context)


def topicsPage(request):
  q=request.GET.get("q") if request.GET.get("q")!=None else ""
  topics=Topic.objects.filter(name__icontains=q)
  return render(request,'base/topics.html',{"topics":topics}) 

def activityPage(request):
  room_messages=Message.objects.all()
  return render(request,'base/activity.html',{'room_messages':room_messages}) 

  