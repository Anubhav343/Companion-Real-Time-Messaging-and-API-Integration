from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import Roomform, Userform, MyUserCreationForm
from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return  redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email' ).lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, "User does not exist.")
            return redirect('login')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:   
            messages.error(request, "Username or password does not match.")

    context = {'page' : page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:   
            messages.error(request, 'Please follow the rules while entering details.')
    context = {'form':  form}
    return render(request, 'base/signup.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms.all()
    topics = Topic.objects.all()
    user_messages = user.user_messages.all()
    context = {'user': user, 'rooms':rooms, 'topics': topics, 'user_messages': user_messages}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    if request.user != user:
        return redirect('user-profile', request.user.id)
    
    form = Userform(instance=user)

    if request.method == "POST":
        form = Userform(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) |
        Q(host__username__icontains = q)
    )
    
    topics = Topic.objects.all()[0:5]
    room_cnt = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains = q)
    )[:5]

    context = {'rooms': rooms, 'topics': topics, 'room_cnt': room_cnt,
               'room_messages': room_messages} 
    return render(request, 'base/home.html', context)


@never_cache
def room(request, pk):
    room = Room.objects.get(id = pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        new_message = Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    messages = room.room_messages.all().order_by('-created')
    participants = room.participants.all()
    context = {'room' : room, 'room_messages': messages, 'participants': participants}
    return render(request, 'base/room.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = Roomform()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    
    action = "Create Room"
    context = {'form' : form, 'topics': topics, 'action': action}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')  
def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    form = Roomform(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here.")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    action = "Update Room"
    context = {'form' : form, 'topics': topics, 'action': action, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:  
        return render(request, 'base/notallowed.html')  
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj' : room})



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this message!")
    
    room_id = message.room.id
    if request.method == 'POST':
        deleted_message_id = message.id
        message.delete()

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_room_{room_id}',
            {
                'type': 'message_deleted_broadcast',
                'message_id': deleted_message_id
            }
        )
        return redirect('room', pk=room_id)
    
    return render(request, 'base/delete.html', {'obj' : message})




def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains = q)
    )

    context = {'topics': topics}
    return render(request, 'base/topics.html/', context)




def activityPage(request):
    rmessages = Message.objects.all()

    context = {'rmessages': rmessages}
    return render(request, 'base/activity.html/',context)