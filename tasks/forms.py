from django import forms
from .models import Task
from django.utils import timezone


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'priority', 'status', 'assigned_to']

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline < timezone.now():
            raise forms.ValidationError('The deadline cannot be in the past.')
        return deadline
