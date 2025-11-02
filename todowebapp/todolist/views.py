from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def get_all_tasks(request):
    context = {
        'fields': [f.name
                    .replace('_', ' ')
                    .capitalize() for f in Task._meta.get_fields() if f.name != 'id'],
        'tasks': Task.objects.all().order_by('-priority')
    }
    return render(request, 'list_todo.html', context)

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("get_all_tasks")
    else:
        form = TaskForm()
    return render(request, "add_task.html", {"form": form})
