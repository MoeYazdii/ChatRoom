from django.shortcuts import render, redirect
from Chatapp.models import Room, Message
from django.http import HttpResponse, JsonResponse
import random
# Create your views here


def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    default_Rand = str(random.randint(0, 999))
    # create a public room at the first

    if not room and not username:
        return redirect(f'/Public/?username={'user'+default_Rand}')
    elif not room:
        return redirect(f'/Public/?username={username}')
    elif not username:
        if Room.objects.filter(name=room).exists():
            return redirect(f'/{room}/?username={'user'+default_Rand}')
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect(f'/{room}/?username={'user'+default_Rand}')
    else:
        if Room.objects.filter(name=room).exists():
            return redirect(f'/{room}/?username={username}')
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect(f'/{room}/?username={username}')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message Sent Successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
