from django.shortcuts import render

# Create your views here.
def render_calendar(request):
    context = {
        'active': 'calendar'
    }
    return render(request, 'calendar.html', context)
