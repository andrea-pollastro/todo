from django.shortcuts import render
from .models import Task

def get_all_tasks(request):
    context = {
        'fields': [f.name
                    .replace('_', ' ')
                    .capitalize() for f in Task._meta.get_fields() if f.name != 'id'],
        'tasks': Task.objects.all().order_by('-priority')
    }
    return render(request, 'list-todo.html', context)
