from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Task
from .forms import TaskForm

def task_list(request):
    # tasks = Task.objects.all().order_by('-priority')
    if request.GET.get('show_completed') == '1':
        tasks = Task.objects.all()
        view = 'all'
    else:
        tasks = Task.objects.exclude(status=2)
        view = 'active'
    tasks = tasks.order_by('-priority')

    context = {
        'tasks': tasks,
        'view': view,
        'form': TaskForm(),
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
