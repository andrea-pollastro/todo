from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all().order_by('-priority')
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    context = {
        'tasks': tasks,
        'fields': ['Status', 'Title', 'Priority', 'Due Date', 'Comment', 'Delivered To', 'Created', 'Updated'],
        'form': form,
    }
    return render(request, 'list_todo.html', context)
