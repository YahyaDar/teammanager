# tasks/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Task created successfully!')
                    return redirect('task_list')
            except Exception as e:
                messages.error(request, f'There was an error creating the task: {e}')
                logger.error(f'Error creating task: {e}')
        else:
            messages.error(request, 'There was an error with the form.')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Task updated successfully!')
                    return redirect('task_list')
            except Exception as e:
                messages.error(request, f'There was an error updating the task: {e}')
                logger.error(f'Error updating task {task_id}: {e}')
        else:
            messages.error(request, 'There was an error with the form.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    try:
        task.delete()
        messages.success(request, 'Task deleted successfully!')
    except Exception as e:
        messages.error(request, f'There was an error deleting the task: {e}')
        logger.error(f'Error deleting task {task_id}: {e}')
    return redirect('task_list')
