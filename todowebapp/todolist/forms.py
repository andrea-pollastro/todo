from django import forms
from .models import Task, Priority

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "due_date", "comment", "delivered_to"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task title"}),
            "priority": forms.Select(choices=Priority.choices, attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional notes"}),
            "delivered_to": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name Surname or Org name"}),
        }
