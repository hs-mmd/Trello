
from django.db import models
from django.contrib.auth.models import User

class Workspace(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    owner   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    members = models.ManyToManyField(User, related_name='workspaces')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Board(models.Model):
    workspace = models.ForeignKey('Workspace',related_name='boards',on_delete=models.CASCADE)
    title     = models.CharField(max_length=100)
    created   = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo',     'To Do'),
        ('doing',    'Doing'),
        ('suspend',  'Suspend'),
        ('done',     'Done'),
    ]

    tags        = models.ManyToManyField(Tag,blank=True, related_name='tasks')
    board       = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date  = models.DateField()
    end_date    = models.DateField()
    due_date    = models.DateField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    assignee    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)


