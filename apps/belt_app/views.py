from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Travel

def index(request):
    return render(request, 'belt_app/index.html')

def register(request):
    requestData = User.objects.register(request.POST)
    if len(requestData['errors']) > 0:
        for error in requestData['errors']:
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['data'] = {
            'uid':requestData['uid'],
            'name':request.POST['name'],
            'username':request.POST['username']
        }
        messages.error(request, requestData['success'])
        return redirect("/travels")

def login(request):
    requestData = User.objects.login(request.POST)
    if len(requestData['errors']) > 0:
        for error in requestData['errors']:
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['data'] = {
            'uid':requestData['uid'],
            'name':requestData['name'],
            'username':request.POST['username']
        }
        messages.error(request, requestData['success'])
        return redirect("/travels")

def logout(request):
    request.session.clear()
    messages.error(request, "You have logged out")
    return redirect('/')

def travels(request):
    if "data" not in request.session:
        return redirect('/')
    you = request.session['data']['uid']
    context = {
        'your_plans':User.objects.get(id=you).trips.all(),
        'our_plans':User.objects.get(id=you).plans.all(),
        'their_plans':Travel.objects.all().exclude(created_by=you).exclude(users=you)
    }
    return render(request, "belt_app/travels.html", context)

def add(request):
    if "data" not in request.session:
        return redirect('/')
    return render(request, "belt_app/add.html")

def add_trip(request):
    if "data" not in request.session:
        return redirect('/')
    requestData = Travel.objects.add_trip(request.POST, request.session['data']['uid'])
    if len(requestData['errors']) > 0:
        for error in requestData['errors']:
            messages.error(request, error)
        return redirect("/travels/add")
    else:
        messages.error(request, requestData['success'])
        return redirect("/travels")

def join(request, tid):
    if "data" not in request.session:
        return redirect('/')
    their_plan = Travel.objects.get(id=tid)
    them = Travel.objects.get(id=tid).created_by.name
    destination = Travel.objects.get(id=tid).destination
    you = User.objects.get(id=request.session['data']['uid'])
    their_plan.users.add(you)
    messages.error(request, "You have joined "+them+" on their trip to "+destination)
    return redirect("/travels")

def destination(request, tid):
    if "data" not in request.session:
        return redirect('/')
    return render(request, "belt_app/destination.html", {'trip':Travel.objects.get(id=tid), 'other_users':Travel.objects.get(id=tid).users.all()})

def user(request, uid):
    if "data" not in request.session:
        return redirect('/')
    name = User.objects.get(id=uid).name
    return render(request, "belt_app/user.html", {'name':name, 'trips':User.objects.get(id=uid).trips.all(), 'more_trips':User.objects.get(id=uid).plans.all()})