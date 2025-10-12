from django.db import models

class Status(models.IntegerChoices):
    NOT_STARTED = 0, 'Not started'
    STARTED = 1, 'Started'
    COMPLETED = 2, 'Completed'

class Priority(models.IntegerChoices):
    LOW = 0, 'Low'
    MEDIUM = 1, 'Medium'
    HIGH = 2, 'High'
    URGENT = 3, 'Urgent'


class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Task(models.Model):
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )
    title = models.CharField(max_length=100)
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    due_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    delivered_to = models.ForeignKey(
        to=Organization, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
