from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .api import WorkspaceViewSet, BoardViewSet, TagViewSet, TaskViewSet

router = DefaultRouter()
router.register('APIworkspaces', WorkspaceViewSet, basename='workspace')
router.register('boards',     BoardViewSet,     basename='board')
router.register('tags',       TagViewSet,       basename='tag')
router.register('tasks',      TaskViewSet,      basename='task')



urlpatterns = [
    path('workspaces/', views.WorkspaceListView.as_view(), name='workspace_list'),
    path('workspaces/create/', views.WorkspaceCreateView.as_view(), name='workspace_create'),
    path('workspaces/<int:pk>/', views.WorkspaceDetailView.as_view(), name='workspace_detail'),
    path('workspaces/<int:workspace_pk>/boards/',views.BoardListView.as_view(),name='board_list'),
    path('workspaces/<int:workspace_pk>/boards/create/',views.BoardCreateView.as_view(),name='board_create'),
    path('workspaces/<int:workspace_pk>/boards/<int:pk>/',views.BoardDetailView.as_view(),name='board_detail'),
    path('workspaces/<int:workspace_pk>/boards/<int:board_pk>/tasks/',views.TaskListView.as_view(),name='task_list'),
    path(
        'workspaces/<int:workspace_pk>/boards/<int:board_pk>/tasks/create/',
        views.TaskCreateView.as_view(),
        name='task_create'
    ),
    path(
        'workspaces/<int:workspace_pk>/boards/<int:board_pk>/tasks/<int:pk>/update/',
        views.TaskUpdateView.as_view(),
        name='task_update'
    ),
    path(
        'workspaces/<int:workspace_pk>/boards/<int:board_pk>/tasks/<int:pk>/delete/',
        views.TaskDeleteView.as_view(),
        name='task_delete'
    ),
    path(
        'workspaces/<int:workspace_pk>/boards/<int:board_pk>/dashboard/',
        views.BoardDashboardView.as_view(),
        name='board_dashboard'
    ),
] + router.urls
