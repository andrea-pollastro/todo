from django.db import models

class Credential(models.Model):
    label = models.CharField(max_length=100)
    username_encrypted = models.TextField()
    password_encrypted = models.TextField()
    notes_encrypted = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label
