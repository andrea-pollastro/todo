from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Task
from .forms import TaskForm

# def task_list(request):
#     tasks = Task.objects.all().order_by('-priority')
#     form = TaskForm()

#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')

#     context = {
#         'tasks': tasks,
#         'fields': ['Status', 'Title', 'Priority', 'Due Date', 'Comment', 'Delivered To', 'Created', 'Updated'],
#         'form': form,
#     }
#     return render(request, 'list_todo.html', context)

def task_list(request):
    # solo GET
    tasks = Task.objects.all().order_by('-priority')
    form = TaskForm()  # form vuoto per il modal
    context = {
        'tasks': tasks,
        'fields': ['Status','Title','Priority','Due Date','Comment','Delivered To','Created','Updated'],
        'form': form,
        'today': timezone.localdate(),
    }
    return render(request, 'list_todo.html', context)

@require_http_methods(["POST"])
def task_create(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('task_list')

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    return redirect('task_list')
