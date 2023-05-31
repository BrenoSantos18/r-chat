from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Message, Topic
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
# Create your views here.

def chatView(request):
    #filter the messages by the topic
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    recent = Room.objects.all()
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        )
    topics = Topic.objects.all()

    room_count = room.count()


    context = {'room':room, 'topics':topics, 'room_count':room_count, 'recent':recent}

    return render(request, 'chatroom/home.html', context)



class ChatDetailView(DetailView):
    model = Room
    template_name = 'chatroom/room_detail.html'


def chatRoom(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    room.participants.add(room.host)

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('chatroom', pk=room.id)

    #filter to display only the childs of room
    messages = room.message_set.all()
    context = {'msg':messages, 'room':room, 'participants':participants}
    return render(request, 'chatroom/chatroom.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You're not the owner")


    if request.method == 'POST':
        message.delete()
        return redirect('chatroom', pk=message.room.id)
    return render(request, "chatroom/delete.html", {'obj':message})






@login_required(login_url='login')
def createRoom(request):
    form = RoomForm

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request, 'chatroom/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You're not the owner")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'chatroom/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You're not the owner")


    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, "chatroom/delete.html", {'obj':room})

