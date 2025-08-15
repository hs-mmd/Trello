
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Workspace, Board, Task
from .forms import WorkspaceForm, BoardForm, TaskForm
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'workspace_list.html'
    context_object_name = 'workspaces'

    def get_queryset(self):
        qs = self.request.user.workspaces.all()
        logger.debug(f'User "{self.request.user}" is retrieving their workspaces. Count: {qs.count()}')
        return qs
    

class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'workspace_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        logger.debug(f"Workspace '{form.instance.name}' is being created by user {self.request.user}.")
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('workspace_detail', kwargs={'pk': self.object.pk})

class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    model = Workspace
    template_name = 'workspace_detail.html'
    context_object_name = 'workspace'

    def dispatch(self, request, *args, **kwargs):
        ws = self.get_object()
        if request.user not in ws.members.all():
            return self.handle_no_permission()
        logger.debug(f"User {request.user} accessed details of workspace id={kwargs.get('pk')}.")
        return super().dispatch(request, *args, **kwargs)

class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board_list.html'

    def get_queryset(self):
        self.workspace = get_object_or_404(Workspace,pk=self.kwargs['workspace_pk'])
        
        if self.request.user not in self.workspace.members.all():
            return self.handle_no_permission()
        
        logger.debug(f"User {self.request.user} requested board list for workspace {self.workspace.id}.")
        return self.workspace.boards.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['workspace'] = self.workspace
        return ctx


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm
    template_name = 'board_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.workspace = get_object_or_404(Workspace,pk=self.kwargs['workspace_pk']
        )
        if request.user not in self.workspace.members.all():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.workspace = self.workspace
        logger.debug(f"User {self.request.user} is creating board '{form.instance.title}' for workspace '{self.workspace.id}'.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board_list', kwargs={'workspace_pk': self.workspace.pk}
        )


class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'board_detail.html'
    context_object_name = 'board'

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, pk=self.kwargs['pk'], workspace__pk=self.kwargs['workspace_pk'])
        if request.user not in self.board.workspace.members.all():
            return self.handle_no_permission()
        
        logger.debug(f"User {request.user} is viewing board id={kwargs.get('pk')}.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['workspace'] = self.board.workspace
        ctx['tasks'] = self.board.tasks.all()
        return ctx


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs['board_pk'], workspace__pk=self.kwargs['workspace_pk']
        )
        if self.request.user not in self.board.workspace.members.all():
            return self.handle_no_permission()
        
        logger.debug(f"User {self.request.user} is viewing task list for board {self.board.id}.")

        return self.board.tasks.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['workspace'] = self.board.workspace
        ctx['board']     = self.board
        return ctx

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board,pk=self.kwargs['board_pk'],workspace__pk=self.kwargs['workspace_pk']
        )
        if request.user not in self.board.workspace.members.all():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['board'] = self.board
        return kw

    def form_valid(self, form):
        form.instance.board = self.board
        logger.debug(f"User {self.request.user} is creating task '{form.instance.title}' in board '{self.board.id}'.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={
                'workspace_pk': self.board.workspace.pk,
                'board_pk':     self.board.pk
            }
        )


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(
            Task,
            pk=self.kwargs['pk'],
            board__pk=self.kwargs['board_pk'],
            board__workspace__pk=self.kwargs['workspace_pk']
        )
        if request.user not in self.task.board.workspace.members.all():
            return self.handle_no_permission()
        
        logger.debug(f"User {self.request.user} is updating task id={self.task.id}.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['board'] = self.task.board
        return kw

    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={
                'workspace_pk': self.task.board.workspace.pk,
                'board_pk':     self.task.board.pk
            }
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(
            Task,
            pk=self.kwargs['pk'],
            board__pk=self.kwargs['board_pk'],
            board__workspace__pk=self.kwargs['workspace_pk']
        )
        if request.user not in self.task.board.workspace.members.all():
            return self.handle_no_permission()
        
        logger.debug(f"User {request.user} want to delete task id={self.task.id}, title='{self.task.title}'.")

        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['board']     = self.task.board
        ctx['workspace'] = self.task.board.workspace
        return ctx
    
    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={
                'workspace_pk': self.task.board.workspace.pk,
                'board_pk':     self.task.board.pk
            }
        )

class BoardDashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        board = get_object_or_404(Board, pk=self.kwargs['board_pk'], workspace__pk=self.kwargs['workspace_pk'])
        ctx['board'] = board

        tasks = Task.objects.filter(board=board)

        now = datetime.now()
        year = now.year
        month = now.month

        monthly_tasks_due = tasks.filter(
            due_date__year=year,
            due_date__month=month
        ).count()
        ctx['monthly_tasks_due'] = monthly_tasks_due

        done_tasks = tasks.filter(status='done').annotate(
            day=TruncDate('due_date')
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        ctx['done_tasks_by_day'] = done_tasks

        total_tasks = tasks.count()
        done_tasks_count = tasks.filter(status='done').count()
        progress = (done_tasks_count / total_tasks) * 100 if total_tasks else 0
        ctx['progress_percent'] = round(progress, 2)

        logger.debug(f"User {self.request.user} is viewing dashboard for board {board.id}.")

        return ctx