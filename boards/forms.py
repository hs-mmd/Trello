
from django import forms
from .models import Workspace,Board, Task, Tag
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple


class WorkspaceForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active = True),
        widget=CheckboxSelectMultiple,
        required=False,
        help_text="Select team members to add."
    )

    class Meta:
        model = Workspace
        fields = ['name', 'members']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields['members'].queryset = User.objects.exclude(pk=current_user.pk)

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title']

class TaskForm(forms.ModelForm):
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
        help_text="Select zero or more labels for this task."
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description',
                  'start_date', 'end_date', 'due_date',
                  'status', 'assignee', 'tags']
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date':   forms.SelectDateWidget,
            'due_date':   forms.SelectDateWidget,
        }

    def __init__(self, *args, board=None, **kwargs):
        super().__init__(*args, **kwargs)
        if board:
            workspace = board.workspace
            qs = workspace.members.all()
            self.fields['assignee'].queryset = qs
        else:
            self.fields['assignee'].queryset = User.objects.none()
