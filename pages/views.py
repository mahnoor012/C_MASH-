from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
#from django.urls import reverse


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import Event
import json
from django.views.decorators.csrf import csrf_exempt


# Landing page
def landing(request):
    return render(request, "landing.html")

# SignUp
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("dashboard1")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard1")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    return redirect("landing")

# Home
def home(request):
    return render(request, "home.html")

# pages/views.py


@login_required
def profile(request):
    if request.method == "POST":
        # user update
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')
    return render(request, 'profile.html')
# about
def about(request):
    return render(request, "about.html")

# contact
def contact(request):
    return render(request, "contact.html")



from .forms import TaskForm
from .models import Task, UserProfile

#dashboard1
@login_required
def dashboard1(request):
    # Get tasks for the logged-in user
    tasks_todo = Task.objects.filter(user=request.user, status='todo')
    tasks_in_progress = Task.objects.filter(user=request.user, status='in_progress')
    tasks_completed = Task.objects.filter(user=request.user, status='completed')
    
    # Process form to add new tasks
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Set the user who added the task
            task.save()
            return redirect('dashboard1')
    else:
        form = TaskForm()

    context = {
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
        'form': form,
        'profile': profile,
    }
    return render(request, 'dashboard1.html', context)


#profilr
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def delete_task(request, task_id):
    # Check if it's a POST request
    if request.method == "POST":
        # Get the task by ID
        task = get_object_or_404(Task, id=task_id)
        task.delete()  # Delete the task
    return redirect('dashboard1')  # Redirect back to the dashboard after deletion



#calender
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Event

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@login_required
def events_json(request):
    events = Event.objects.filter(user=request.user)
    data = []
    for e in events:
        data.append({
            "id": e.id,
            "title": e.title,
            "start": str(e.start_date),
            "end": str(e.end_date),
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def add_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        start = data.get("start")
        end = data.get("end")
        event = Event.objects.create(
            user=request.user,
            title=title,
            start_date=start,
            end_date=end
        )
        return JsonResponse({"status": "ok", "id": event.id})
    return JsonResponse({"status": "error"})

@csrf_exempt
@login_required
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id, user=request.user)
        event.delete()
        return JsonResponse({"status": "deleted"})
    except Event.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Not found"})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WebsiteForm
from .models import Website

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.owner = request.user
            site.save()
            return redirect('dashboard')
    else:
        form = WebsiteForm()

    websites = Website.objects.filter(owner=request.user).order_by('-created')
    return render(request, 'dashboard.html', {'form': form, 'websites': websites})

@login_required
def delete_website(request, website_id):
    website = get_object_or_404(Website, id=website_id, owner=request.user)
    website.delete()
    return redirect('dashboard')



