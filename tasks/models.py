from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=PRIORITY_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', null=True, blank=True, on_delete=models.SET_NULL)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_completed_within_deadline(self):
        if self.completed_at and self.completed_at <= self.deadline:
            return True
        return False

    @property
    def is_completed(self):
        return self.status == 'completed'
