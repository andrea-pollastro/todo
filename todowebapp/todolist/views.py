from django.shortcuts import render
from .models import Task

# Create your views here.
def index(request):
    context = {
        'fields': [f.name
                    .replace('_', ' ')
                    .capitalize() for f in Task._meta.get_fields() if f.name != 'id'],
        'tasks': Task.objects.all()
    }
    return render(request, 'list-todo.html', context)
