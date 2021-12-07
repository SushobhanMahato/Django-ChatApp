from django.shortcuts import render, redirect
from chatapp.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def home1(request):
    return render(request, 'home1.html')

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
    user = request.user
    username1 = user.username
    if username==username1:
        if Room.objects.filter(name=room).exists():
            return redirect('/'+room+'/?username='+user.first_name)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect('/'+room+'/?username='+user.first_name)
    else:
        messages.info(request,'wrong username')
        return redirect('home1')

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    ok = 0
    for s in message:
        if s != " ":
            ok=1
            break
    if message != "" and ok:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return HttpResponse('Message sent successfully')
    else:
        return HttpResponse('Unable to send')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

#user account

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        passward=request.POST['password']
        user = auth.authenticate(username=username, password=passward)    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'wrong username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        passward1=request.POST['password1']    
        passward2=request.POST['password2']    
        
        if passward1==passward2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username, password=passward1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'passward not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')